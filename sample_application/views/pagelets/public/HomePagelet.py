'''
	Pagelet for a sample Home Page
	
	Author: Andrew Oberlin
	Date: August 20, 2012
'''
from renderEngine.PageletBase import PageletBase
from mycoplasma_home.chado import Organism

class HomePagelet(PageletBase):
	'''
		Renders the center of the home page		
	
		Params: request -- the Django request object with the POST & GET args
		
		Returns: Dictionary of arguments for rendering this pagelet
	'''
	def doProcessRender(self, request):
		self.setLayout('public/home.html')

		# Return here a dictionary of arguments that should
		# be passed into the template rendered by Django
		return {}
