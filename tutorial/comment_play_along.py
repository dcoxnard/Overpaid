from scrapy.selector import Selector
import re

regex = re.compile(r'<!--(.*)-->', re.DOTALL)

a = response.xpath('//comment()').re(regex)

for i in range(len(a)):
    comment = response.xpath('//comment()').re(regex)[i]
    commentsel = Selector(text=comment, type='html')
    print(commentsel.xpath('//table[@id="pitching_value"]').extract_first())

    #Index 16 is the one with the disgusting stuff.
    commented_text = response.xpath('//comment()').re(regex)[16]
    new_selector = Selector(text=commented_text, type='html')
    salary = new_selector.xpath('//td[@data-stat="Salary"]/text()').extract_first()