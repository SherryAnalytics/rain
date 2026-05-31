---
layout: page
title: Garden of Thoughts
permalink: /garden-of-thoughts/
---

A growing collection of observations on data, AI, cloud and the craft of analytics.

{% assign posts = site.collections | where: "label", "garden-of-thoughts" | first %}
{% for post in posts.docs reversed %}
- [{{ post.title }}]({{ post.url }}) — {{ post.date | date: "%B %d, %Y" }}
{% endfor %}
