---
layout: page
title: Garden of Thoughts
---

A growing collection of observations on data, AI, and the craft of analytics.

{% for post in site.garden-of-thoughts reversed %}
- [{{ post.title }}]({{ post.url }}) — {{ post.date | date: "%B %d, %Y" }}
{% endfor %}
