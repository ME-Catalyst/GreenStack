/**
 * DocsSearchEngine - Full-text search system for documentation
 *
 * Features:
 * - Fuzzy matching for typo tolerance
 * - Keyword boosting
 * - Title/description priority scoring
 * - Category filtering
 * - Result ranking
 * - Auto-complete suggestions
 * - Related content recommendations
 */

class DocsSearchEngine {
  constructor() {
    this.index = [];
    this.documents = new Map();
  }

  /**
   * Build search index from documentation pages
   * @param {Array} pages - Array of page metadata objects
   */
  buildIndex(pages) {
    this.index = [];
    this.documents.clear();

    pages.forEach(page => {
      const doc = {
        id: page.id,
        title: page.title,
        description: page.description || '',
        content: page.content || '',
        keywords: page.keywords || [],
        category: page.category || '',
        url: page.url || `/docs/${page.id}`,
        headings: page.headings || [],
        lastUpdated: page.lastUpdated || new Date().toISOString()
      };

      this.documents.set(page.id, doc);
      this.index.push(doc);
    });
  }

  /**
   * Calculate Levenshtein distance for fuzzy matching
   * @param {string} a - First string
   * @param {string} b - Second string
   * @returns {number} - Edit distance
   */
  levenshteinDistance(a, b) {
    const matrix = [];

    for (let i = 0; i <= b.length; i++) {
      matrix[i] = [i];
    }

    for (let j = 0; j <= a.length; j++) {
      matrix[0][j] = j;
    }

    for (let i = 1; i <= b.length; i++) {
      for (let j = 1; j <= a.length; j++) {
        if (b.charAt(i - 1) === a.charAt(j - 1)) {
          matrix[i][j] = matrix[i - 1][j - 1];
        } else {
          matrix[i][j] = Math.min(
            matrix[i - 1][j - 1] + 1,
            matrix[i][j - 1] + 1,
            matrix[i - 1][j] + 1
          );
        }
      }
    }

    return matrix[b.length][a.length];
  }

  /**
   * Check if query matches text with fuzzy tolerance
   * @param {string} query - Search query
   * @param {string} text - Text to match against
   * @param {number} threshold - Fuzzy match threshold (0-1)
   * @returns {boolean} - Whether match is found
   */
  fuzzyMatch(query, text, threshold = 0.8) {
    const lowerQuery = query.toLowerCase();
    const lowerText = text.toLowerCase();

    // Exact match
    if (lowerText.includes(lowerQuery)) {
      return true;
    }

    // Word-by-word fuzzy matching
    const queryWords = lowerQuery.split(/\s+/);
    const textWords = lowerText.split(/\s+/);

    return queryWords.some(queryWord => {
      return textWords.some(textWord => {
        const distance = this.levenshteinDistance(queryWord, textWord);
        const maxLength = Math.max(queryWord.length, textWord.length);
        const similarity = 1 - (distance / maxLength);
        return similarity >= threshold;
      });
    });
  }

  /**
   * Calculate relevance score for a document
   * @param {Object} doc - Document object
   * @param {string} query - Search query
   * @returns {number} - Relevance score (0-100)
   */
  calculateScore(doc, query) {
    const lowerQuery = query.toLowerCase();
    let score = 0;

    // Title match (highest priority) - 40 points
    if (doc.title.toLowerCase().includes(lowerQuery)) {
      score += 40;
    } else if (this.fuzzyMatch(query, doc.title, 0.8)) {
      score += 20;
    }

    // Description match - 25 points
    if (doc.description.toLowerCase().includes(lowerQuery)) {
      score += 25;
    } else if (this.fuzzyMatch(query, doc.description, 0.8)) {
      score += 12;
    }

    // Keyword match - 20 points
    const keywordMatch = doc.keywords.some(keyword =>
      keyword.toLowerCase().includes(lowerQuery) ||
      this.fuzzyMatch(query, keyword, 0.8)
    );
    if (keywordMatch) {
      score += 20;
    }

    // Content match - 15 points
    if (doc.content.toLowerCase().includes(lowerQuery)) {
      score += 15;
    } else if (this.fuzzyMatch(query, doc.content, 0.7)) {
      score += 7;
    }

    // Heading match - 10 points
    const headingMatch = doc.headings.some(heading =>
      heading.text.toLowerCase().includes(lowerQuery) ||
      this.fuzzyMatch(query, heading.text, 0.8)
    );
    if (headingMatch) {
      score += 10;
    }

    return score;
  }

  /**
   * Search documentation
   * @param {string} query - Search query
   * @param {Object} options - Search options
   * @returns {Array} - Array of search results
   */
  search(query, options = {}) {
    const {
      category = null,
      limit = 10,
      minScore = 10
    } = options;

    if (!query || query.trim().length === 0) {
      return [];
    }

    const results = [];

    for (const doc of this.index) {
      // Category filtering
      if (category && doc.category !== category) {
        continue;
      }

      const score = this.calculateScore(doc, query);

      if (score >= minScore) {
        results.push({
          ...doc,
          score,
          highlights: this.getHighlights(doc, query)
        });
      }
    }

    // Sort by score (descending)
    results.sort((a, b) => b.score - a.score);

    return results.slice(0, limit);
  }

  /**
   * Get highlighted text snippets for search results
   * @param {Object} doc - Document object
   * @param {string} query - Search query
   * @returns {Array} - Array of highlighted snippets
   */
  getHighlights(doc, query) {
    const highlights = [];
    const lowerQuery = query.toLowerCase();

    // Check title
    if (doc.title.toLowerCase().includes(lowerQuery)) {
      highlights.push({
        type: 'title',
        text: doc.title
      });
    }

    // Check description
    if (doc.description.toLowerCase().includes(lowerQuery)) {
      highlights.push({
        type: 'description',
        text: doc.description
      });
    }

    // Check content (first match only)
    const contentIndex = doc.content.toLowerCase().indexOf(lowerQuery);
    if (contentIndex !== -1) {
      const start = Math.max(0, contentIndex - 50);
      const end = Math.min(doc.content.length, contentIndex + query.length + 50);
      highlights.push({
        type: 'content',
        text: '...' + doc.content.substring(start, end) + '...'
      });
    }

    return highlights;
  }

  /**
   * Get auto-complete suggestions
   * @param {string} partial - Partial query
   * @param {number} limit - Maximum number of suggestions
   * @returns {Array} - Array of suggestions
   */
  suggest(partial, limit = 5) {
    if (!partial || partial.length < 2) {
      return [];
    }

    const lowerPartial = partial.toLowerCase();
    const suggestions = new Set();

    for (const doc of this.index) {
      // Title suggestions
      if (doc.title.toLowerCase().startsWith(lowerPartial)) {
        suggestions.add(doc.title);
      }

      // Keyword suggestions
      doc.keywords.forEach(keyword => {
        if (keyword.toLowerCase().startsWith(lowerPartial)) {
          suggestions.add(keyword);
        }
      });

      // Word-level suggestions from title
      const titleWords = doc.title.split(/\s+/);
      titleWords.forEach(word => {
        if (word.toLowerCase().startsWith(lowerPartial)) {
          suggestions.add(word);
        }
      });
    }

    return Array.from(suggestions).slice(0, limit);
  }

  /**
   * Get related documents based on similarity
   * @param {string} docId - Document ID
   * @param {number} limit - Maximum number of related documents
   * @returns {Array} - Array of related documents
   */
  getRelated(docId, limit = 3) {
    const doc = this.documents.get(docId);
    if (!doc) {
      return [];
    }

    const related = [];

    for (const otherDoc of this.index) {
      if (otherDoc.id === docId) {
        continue;
      }

      let score = 0;

      // Category similarity (40 points)
      if (otherDoc.category === doc.category) {
        score += 40;
      }

      // Keyword overlap (30 points)
      const commonKeywords = doc.keywords.filter(k =>
        otherDoc.keywords.includes(k)
      ).length;
      score += Math.min(30, commonKeywords * 10);

      // Content similarity (30 points) - simple word overlap
      const docWords = new Set(doc.content.toLowerCase().split(/\s+/));
      const otherWords = otherDoc.content.toLowerCase().split(/\s+/);
      const commonWords = otherWords.filter(w => docWords.has(w)).length;
      score += Math.min(30, commonWords / 10);

      if (score > 20) {
        related.push({ ...otherDoc, score });
      }
    }

    // Sort by score
    related.sort((a, b) => b.score - a.score);

    return related.slice(0, limit);
  }

  /**
   * Get all categories
   * @returns {Array} - Array of unique categories
   */
  getCategories() {
    const categories = new Set();
    this.index.forEach(doc => {
      if (doc.category) {
        categories.add(doc.category);
      }
    });
    return Array.from(categories).sort();
  }

  /**
   * Get document by ID
   * @param {string} id - Document ID
   * @returns {Object|null} - Document object or null
   */
  getDocument(id) {
    return this.documents.get(id) || null;
  }
}

// Create singleton instance
export const searchEngine = new DocsSearchEngine();

export default DocsSearchEngine;
