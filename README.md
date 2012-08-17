DjangoPagelets
==============

An extension of Django to add Pagelet/Application Functionality

Using Django's application model with views and models. This rendering engine/file structure
allows the user to make even more reuse of the code base by adding a pagelet/application layer
to the rendering engine.

An application directly links to a web address in the urls.py the way any view would. However, its
rendering is done through an engine on top of Django's rendering engine. An example application file
can be found at django_project/django_app/renderEngine/ApplicationBase.py. All applications would extend
this class or another that has been made on top of this class.

Applications render application layouts, which are html files residing in the templates folder under
the Django app. These layouts are made to only include the underlying structure of the page. An example layout:

<html>
  <head>
    <link rel="stylesheet" type="text/css" src="/css/style.css" />
    <script type="text/javascript" src="/js/jquery.min.js"></script>
  </head>
  <body>
    <div>
      <renderSlot name="navBar" />
    </div>
    <div>
      <renderSlot name="center" />
    </div>
  </body>
</html>

Applications then fill these "renderSlots" with pagelets.

Pagelets are the core of the website and display information to the user. The web page would just be a shell without
them. These pagelets have a doProcessRender method in which one would return a dictionary for rendering to a context.
This is similar to a view function; however, these are individualized per pagelet rather than per page.

The pagelet layout will look like an ordinary template and reside in the templates/pageletLayouts directory. These are 
rendered the same as the traditional Django template.