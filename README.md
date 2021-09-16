# NutCompany_FlaskApp

This app developed for company that makes fruits.

**Technical assignment** includes:
* Admin panel with developing desing ( at least moqup). 
* Public pages with info about company, news, gallery
* Online shop functionality

Main framework **Flask** with extenstion like **FlaskWTF**


For admin page i user ***AdminLte*** package, which includes html template and javascript/css plugins.  


But, because Flask, even with extension, has lots of restriction i had to implement some functionality by myself. 

For example, **generic** mixin for CRUD operations. This helps me to avoid code duplicating. 

Another example is **formset** conseptions which i took from Django. It is about handling multiple forms in one page. 

Class **Formset** is used for multiple forms in one page and **InlineFormset** if this forms depend on another instance like Parent->Child (For example: AboutCompany(Parent) and Gallery(Child))

Also, i use JavaScript to make formset dynamic.   
