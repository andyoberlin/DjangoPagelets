'''
	Application for the Image Editor of the DOME
	URL: / or /index.html
	
	Author: Andrew Oberlin
	Date: August 20, 2012
'''
from renderEngine.ApplicationBase import ApplicationBase
from sample_application.views.pagelets.public.HomePagelet import HomePagelet

class Application(ApplicationBase):
	def doProcessRender(self, request):
		self.setApplicationLayout('public/base.html')
		self.addPageletBinding('home', HomePagelet())

'''
	Used for mapping to the url in urls.py
'''        	
def renderAction(request):
	return Application().render(request)

