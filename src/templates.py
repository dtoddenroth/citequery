#!/usr/bin/env python3

index = """<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8"/>
		<link rel="stylesheet" href="/static/style.css?v=4"/>
		<title>{caption}</title>
	</head>
	<body class="{layout}">
		<h2>{caption}</h2>
		{content}
	</body>
</html>
"""

citation = """
<div class="citation">
{citing} cite {cited}
</div>
"""

citationtext = "{authors} {journal} {year}"

citing = """
<div class="citing">
	<a href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/" target="_new">
		<span class="title">{title}</span>
		<span class="authors">{authors}</span>
		<span class="journal">{journal}</span>
		<span class="year">({year})</span>
	</a>
</div>
"""

cited = """
<div class="cited">
	<a href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/" target="_new">
		<span class="title">{title}</span>
		<span class="authors">{authors}</span>
		<span class="journal">{journal}</span>
		<span class="year">({year})</span>
	</a>
</div>
"""

examples = """
	try {examples}, or other 
	<a href="https://pubmed.ncbi.nlm.nih.gov/" target="_new">pubmed</a>
	queries
"""

resultfreqs = """
	found {ncitations} citations of {ncited} articles 
	(<a href="/rss?query={query}">rss</a>, 
	<a href="/api?query={query}">json</a>)
"""

mainform = """
<div class="form"><form action="/search" class="form">
	 <input type="search" class="searchinput"
	 	name="query" size="40" value='{query}'/>
	 <input type="submit" class="submitinput" value="search"/>
</form></div>
<div class="status">
	{status}
</div>
<div class="results">
	{results}
</div>
"""

rssframe = """<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
	<atom:link href="{serveraddress}rss?query={query}" 
		rel="self" type="application/rss+xml" />
	<title>Citations of '{query}'</title>
	<link>{serveraddress}rss?query={query}</link>
	<description>Citations of '{query}'</description>
	{items}
</channel>
</rss>
"""

rssitem = """
<item>
	<title>{title}</title>
	<description>{description}</description>
	<link>https://pubmed.ncbi.nlm.nih.gov/{pmid}/</link>
	<guid isPermaLink="false">{itemid}</guid>
	<author>{author}</author>
	<pubDate>{pubDate}</pubDate>
</item>
"""

rssdescription = """
	<p>{citing} cite {cited}:</p> 
	<h3>{title}</h3> 
	<p>{abstract}</p>  
	<p>PMID: {pmid}</p>
""".replace(">","&gt;").replace("<","&lt;")

