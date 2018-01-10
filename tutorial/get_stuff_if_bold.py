## Need to have the spider not skip players with names in a <b> tag.
## Also need to implement filter for only active players from 2000 onward.

for p in player_div.xpath('./p'):
    active = p.xpath('./text()').extract()
    player = p.xpath('./a/text()').extract()
    href = p.xpath('./a/@href').extract()
    if not player:
         active_bold = p.xpath('./b/text()').extract()
         player_bold = p.xpath('./b/a/text()').extract()
         href = p.xpath('./b/a/@href').extract()
    	print(player_bold, active_bold, href)     
    else:
    	print(player, active, href)