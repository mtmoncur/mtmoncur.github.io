---
title: Issue-Branch Converter
excerpt: Convert GitHub Issue Names to Branch Names
header:
  teaser: assets/img/stock-photos/alain-wong-59855-unsplash.png
  overlay_image: assets/img/stock-photos/alain-wong-59855-unsplash.png
  overlay_filter: 0.1
---

### Issue Name

<input type="text" placeholder="My Super Very Long Issue Title" id="input">

<input class="btn btn--primary" type="submit" value="Convert"
onclick="document.getElementById('input').value =
document.getElementById('input').value.toLowerCase().replace(/[^a-z\d\s]/g, '').trim().replace(/\s/g,'-');return false;">

## Example Usage
Given the following issue name:

`# TODO: remove type ignore when mypy supports numpy #261`

It will be converted to the following:

`todo-remove-type-ignore-when-mypy-supports-numpy-261`