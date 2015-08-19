import urllib
import re
import sys

'''
	example:
	to search patagonia adze jacket run:
	python searchsnc.py patagonia adze jacket
'''

def findproduct(wants):
	f = urllib.urlopen('http://www.steepandcheap.com')
	html = f.read()
	collecturls = re.findall(r'<a class=\"collection-link\" href=\"(.+)\">',str(html))

	prog = re.compile(r"""\{\"collectionSkuClass\"\:\"(.*?)\"\,
							\"collectionClassId\"\:(.*?)\,
							\"skuClass\"\:\"(.*?)\"\,
							\"qtyRemaining\"\:(.*?)\,
							\"price\"\:(.*?)\,
							\"retailPrice\"\:(.*?)\,
							\"discount\"\:(.*?)\,
							\"name\"\:\"(.*?)\"\,
							\"brand\"\:(.*?)\,
							\"defaultImage\"\:(.*?)\,
							\"facets\"\:\{(.*?)\}\}
		""",re.X)

	productnames = []
	prices = []
	qty = []
	links = []
	discount = []
	brands = []
	size = []
	gender = []

	for collecturl in collecturls:
		collectlink = 'http://www.steepandcheap.com'+collecturl
		f = urllib.urlopen(collectlink)
		html = f.read()
		products = prog.findall(html)
		for product in products:
			if product[3]!='0':
				iswant = 0
				for want in wants:
					if str(want).lower() in str(product[7]).lower() or str(want).lower() in str(product[8]).lower() or str(want).lower() in str(product[10]).lower():
						iswant = iswant + 1
				if iswant==len(wants):
					productnames.append(product[7])
					prices.append(float(product[4]))
					qty.append(int(product[3]))
					links.append(collectlink+'/'+product[0])
					discount.append(float(product[6]))
					brand = re.findall(r'\"name\":\"(.*?)\"',product[8])
					brands.append(brand[0])
					gender.append(product[10])

	num = 0
	for brand in brands:
		print productnames[num],'\t',prices[num],'\t',discount[num],'\t',brands[num]
		print links[num]
		num = num+1

def main():
	args = sys.argv[1:]
	if not args:
		args.append('nothing')
	findproduct(args)

if __name__ == '__main__':
	main()


