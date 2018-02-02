部分一：基于RBAC的权限管理

部分二：用flask-admin组件批量完成model的CRUD操作。

以下记录自己在完成过程中遇到的问题，以及解决办法。

flask-admin组件：
1.实现删除的过程中，出现 sqlalchemy.orm.exc.StaleDataError: DELETE statement on table 'role2permission' expected to delete 2 row(s); Only 0 were matched 提示，并且删除失败。

-- 解决办法：在model类中，添加属性 __mapper_args__ = {'confirm_deleted_rows': False} 
