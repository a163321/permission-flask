部分一：基于RBAC的权限管理

部分二：用flask-admin组件批量完成model的CRUD操作。

以下记录自己在完成过程中遇到的问题，以及解决办法。

flask-admin组件：1.在组件实例化的时候，设置
flask_admin = Admin(base_template='admin/base_menu.html')

2.要覆盖任何内置模板，只需将它们从Flask-Admin源代码复制到项目的templates/admin /目录中即可。 只要文件名保持不变，项目目录中的模板应该自动优先于内置模板。

3.模板继承顺序：
	--admin_base_template(也就是base_menu.html)，这个模板可以是设置的，就是在第一步的时候设置的，我们这里设置了之后，就全覆盖了，

	--master.html ,源码中，这个模板是继承自admin_base_template，也就是在源码中的base.html页面(..\flask_admin\templates\bootstrap3\admin\base.html)
		--源码中，这个模板就是一句话：{% extends admin_base_template %}
		
	--其他注册的模板，都是继承自master.html的.
	
	--我们这里的逻辑是直接用自己的模板base_menu.html(为了接受变量，我这里直接把源码中的base.html页面的东西拷贝到base_menu.html中，然后开始自己的改造)

4.我们的改造:
	--添加上我们自己的导航栏、左侧菜单栏，然后把模板中，我们base.html中我们需要的的东西拷贝到我们的content部分中，

​	
​	
5.遇到的问题：
	--在编辑角色时，TypeError: __str__ returned non-string (type NoneType)
	在sqlchemy的model表中，加上,__mapper_args__ = {‘confirm_deleted_rows': False}
	
	--在删除多对多管理的时候，报错：Failed to delete record. DELETE statement on table 'role2permission' expected to delete 1 row(s); Only 0 were matched.
	解决方法：在sqlchemy的model表中，在有secondary的地方这样写；relationship('xxx',secondary='xxx2yyy',backref='xx',passive_deletes=True)，一定写passive_deletes=True，passive_deletes: 支持关联(被动)删除，设置为True
	 
	--在添加(create)报错：TypeError: __str__ returned non-string (type NoneType)
	解决方法：数据库中存在空值，所以会是NoneType,记得在数据库中设定字段不能为空。