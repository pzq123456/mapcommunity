# mapcommunity
这是WEBGIS大作业：地图社区（mapcommunity）
基于flask、百度地图api编写。主要功能参考了Miguel Grinberg的blog（https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world）。
具体实现了用户注册、登录、留言、跟帖等功能。

比较创新的点：将用户帖子视图与地图视图作为<iframe>窗口插入到主页面中，在不改变页面比例的前提下实现了用户帖子的瀑布式展示；
             结合百度地图api的信息窗口，实现了地图上点击即可留言，鼠标悬停即可跟帖；
不足：两个<iframe>之间的交互不足，前端还需补充js功能；
      可玩性不足，无法激发用户的发帖欲望；
  
  Hi! This is map_community,a forum based on flask(&its plug-ins)and baidumapAPI.In this forum you can register,post,follow_post,follow_someone and ,the most interesting function,do all of those in map view!
