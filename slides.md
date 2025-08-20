---
marp: true
theme: uncover
paginate: true
header: 'Product Documentation: API v2.0'
footer: '© 2025 Software Inc. | Contact: 23f2005593@ds.study.iitm.ac.in'

# Custom theme styles are defined here.
style: |
  .slide {
    font-family: 'Arial', sans-serif;
  }
  h1 {
    color: #005A9C;
    text-align: center;
  }
  h2 {
    color: #0078D4;
    border-bottom: 2px solid #0078D4;
  }
  .quote {
    color: #555;
    font-style: italic;
    text-align: center;
    border-left: 5px solid #ccc;
    padding-left: 20px;
  }
---

<!-- _class: lead -->
<!-- _backgroundColor: #f0f4f8 -->

# **API v2.0 Product Documentation**
## A Guide for Developers
Technical Writer Team

---

## Agenda

1.  **Introduction**: What's new in API v2.0?
2.  **Key Features**: A detailed look at new endpoints.
3.  **Performance**: Algorithmic improvements.
4.  **Migration**: Steps to upgrade from v1.0.
5.  **Q&A**

---

<!--
# This slide now uses a local image from the 'images' folder.
backgroundImage: "url('photo.jpg')"
backgroundSize: cover
_color: white
_textShadow: 1px 1px 5px black
-->

## Key Features Overview

- **New Endpoint**: `/users/profile` for aggregated user data.
- **Enhanced Security**: OAuth 2.0 is now mandatory.
- **Batch Operations**: Support for bulk record creation.

---

## Performance Improvements

We have optimized our core sorting algorithm. The new implementation reduces the time complexity for average cases.

The previous version had a complexity of:
$$ O(n^2) $$

The new version improves this to:
$$ O(n \log n) $$

This results in a significant performance gain on large datasets.

---

<!-- _backgroundColor: #e8f5e9 -->

## Migration from v1.0

<div class="quote">
  "The migration process is designed to be as seamless as possible."
</div>

**Key Steps:**
1.  Update base URL to `https://api.example.com/v2/`.
2.  Replace API key authentication with an OAuth 2.0 token.
3.  Test deprecated endpoints and update to their v2.0 equivalents.

---

## Thank You

**Questions?**
