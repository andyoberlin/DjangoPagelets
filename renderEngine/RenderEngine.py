'''
    Render Engine for Django
	
	Author: Andrew Oberlin
	Date: August 20, 2012
'''
import re
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
import simplejson as json

class RenderEngine:
	'''
		Initialize the rendering system
	'''
	def __init__(self, ):
	    # correctly sets the pagelet and application layouts
	    # based on the settings in the main application
		self.pageletMap = dict()
		
		# makes sure that this directory ends in a slash
		self.layoutDir = settings.APPLICATION_LAYOUT_DIR
		if (self.layoutDir[len(self.layoutDir) - 1] != '/'):	
			self.layoutDir = self.layoutDir + '/'
			
		# makes sure that this directory ends in a slash
		self.pageletDir = settings.PAGELET_LAYOUT_DIR
		if (self.pageletDir[len(self.pageletDir) - 1] != '/'):
			self.pageletDir = self.pageletDir + '/'
		
	
	'''
		Sets the application layout for this rendering engine
		
		@param: applicationLayout -- the layout for the application
	'''
	def setApplicationLayout(self, applicationLayout):
		self.applicationLayout = applicationLayout
	
	'''
		Binds the pageletFile to the pageletName
		
		@param: pageletName -- the name attribute to look for in the renderSlot
		@param: pageletObj -- the pagelet object to bind this name to
	'''
	def addPageletBinding(self, pageletName, pageletObj):
		self.pageletMap[pageletName] = pageletObj
	
	'''
	    Renders a single pagelet by searching for the name of the pagelet
	    and then if it is not found renders an error message
	    
	    @param: pageletAttr -- the attributes in the renderSlots (needs the name attribute)
	    @param: request -- the Django request object sent
	    @param: layout -- the application layout in which this pagelet belongs
	    @param: pos -- the position of this tile in the application layout
	    @param: last -- boolean flag saying if this is the last tile 
	    
	    @return: Returns the pagelet rendered to the context to which it is bound
	'''
	def renderPagelet(self, pageletAttr, request, layout, pos, last):
		propertyPattern = re.compile(r'(?i)name="(.+?)"')
		pageletName = propertyPattern.search(pageletAttr).group(1)
		if (self.pageletMap.has_key(pageletName)):
			pagelet = self.pageletMap[pageletName]
			context = RequestContext(request, pagelet.doProcessRender(request))
			context['SITE_URL'] = settings.SITE_URL
			context['STATIC_URL'] = settings.STATIC_URL
			pageletRendered = render_to_string(self.pageletDir + pagelet.getLayout(), context_instance=context)
			renderTile = layout[pos[2]:pos[0]] + pageletRendered
			if (last):
				renderTile += layout[pos[1]:]
			return renderTile
		else:
			return '<b>Pagelet ' + pageletName + ' has no binding</b>'
	
	'''
	    Renders an application based on the request made and the application
	    layout that has been set and the pagelet bindings that have been made
	    
	    @param: request -- the Django request object that has been made
	'''			
	def render(self, request):
		layout = render_to_string(self.layoutDir + self.applicationLayout, {})
		
		# Regex for finding the renderSlots which look like this:
		# <renderSlot name="<pagelet_name>" />
		renderSlotPattern = re.compile(r"(?i)<renderSlot(.+?)/>")
		patIter = renderSlotPattern.finditer(layout)
		matches = [match for match in patIter]	
	
		lastIndex = len(matches)
		lastEnd = 0
		tiles = list()
		lastIndex -= 1
		
		# renders the page in tiles in sequence and adds to one string
		for (count, match) in enumerate(matches):
			last = count == lastIndex
			attr = match.group(1)
			pos = (match.start(0), match.end(0), lastEnd)
			tiles.append(self.renderPagelet(attr, request, layout, pos, last))
			lastEnd = match.end(0)
		
		# aggregates all the tiles into one string
		layout = ''.join(tiles)
		
		return HttpResponse(layout)
    
    '''
        An alternative render option that will render json from python objects. 
        Very useful for ajax which should not require a pagelet, but should be 
        instead treated like a service call
        
        @param: request -- the Django request object that has been made
    '''
	def renderJson(self, request):
		return HttpResponse(json.dumps(self.applicationLayout))
