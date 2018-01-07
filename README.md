###1.客户信息：  
（1）客户信息中有公共客户，自己的客户。而公共客户属于新录入的客户和在规定的时间中某个业务人员没有完成的。假如：规定在3天业务人员和客户没有进行跟进或者是在15天没有完成这个订单并且没有报名，那么这个客户就会属于公共资源，那么就是当前时间减去15天它如果大于你接单的时间或者当前时间减去3天它大于最后的跟进的时间，那么他就属于公共客户资源（通过Q对象把这个条件构造出来），这客户你就在无权去访问。  
（2）我的客户就是在自己这里成单或者是在这15天自己跟进的客户，而在这期间在创建一个客户分配表，分配表中包括它的状态，接单时间，以及客户的ID和课程顾问的ID。生成一条记录。如果新来一个客户，那么设计一个定时任务，这个定时就好每天在规定的时间的让这个脚本跑一次，那么这个数据它会在每天定时更新，它具体的功能是：执行py文件：操作两张表，查找客户表，找到它的公共资源，查找分配表中的数据，并更新状态（3天/15天）。而在事实定时有两种方案：一是：可以通过原生的SQL写，也可以通过django也可以写（必须把定时任务和django放在一起使用，）当前用户所有的客户具体实现：创建一个url，首先在session中获取当前用户登录的ID,根据当前用户登录的ID去表中获取他自己的数据（custmers=models.CustomerDistribution.objects.filter(user_id=current_user_id).order_by('status')）把正在跟进的排在前面已成单的放在最后面
（3）在新建的选出没有报名的客户，在没有报名的客户后面加上抢单这个功能，获取当前用户的ID，把客户表中的客户修改，并把接单时间修改成当前时间，把跟进时间也改成当前时间，把原来的课程顾问改为现在跟进的课程顾问，把这些修改的数据更新到数据库中（更新时注意，原顾问不是自己，状态是没报名15天没有成单的，才可以跟新）。在分配表中创建一条数据。

#####2.自动抢单：  
（1） 单条录入：先创建一个url，首先get看到一个页面，（用modelform写一个页面），客户表中新增数据：一获取改分配的课程顾问的id,以及当前的时间，客户分配表新增数据，获取新创建的客户的ID，顾问的ID。该分配的 课程顾问：就是按照权重以及按照分配表的的排序来分配，用迭代器来实现，数据库必须存在每个人的权重，在数据中在创建一个销售权重表表中有个数以及权重。先创建一个文件，在这个文件中写一个静态字段（静态字段包括user，iter_users，reset_status），下来就是跟中权重在数据库中来去符合的数据（数据就是销售）把数据库中拿到的数据跟新到静态字段中的user中，iter_users是生成迭代器的。  

3.学生业务  

共有三张表：学生表，上课记录表，班级表  

学习记录：  
为什么要用初始化：这样做起来方便，批量初始一些数据。  
单个的初始化学生：
　　刚开始设置学生上课记录的初始化功能，在上课记录这张表中拿到班级的ID来找到这个班级所有的学生，循环这个班的所有学生，这样就可以拿到每一个学生，为每一个学生生成每一天的学习记录。这样就是对每一个学生进行了上课的初始化。
批量初始化操作：
　　设置一个action（可以有返回值），在上课记录这张表中拿到这个上课记录的对象。循环拿到每一个上课记录，为一个学生创建学习记录（在创建学习记录是在学生学习记录表中
查看这个学生是否有学习记录如果有，就不让他创建，如果没有就让他创建），
考勤管理：
上课时有多少人，把学生罗列出来。设置action(action里面有缺勤，迟到，早退，签到，请假)，以缺勤来说，默认是签到，拿到id，把拿到的数据更新

 

4.微信提醒

目的：让员工关注公司的推送消息公众号，并绑定个人用户(用于以后的消息提醒)
　　第一步：扫码关注服务号
　　第二部：扫码绑定个人账户，扫码的同时，个人的openid会自动录入到数据库中

在用户表中，获取到用户的openid，就能发送微信消息

class UserInfo(models.Model):
　　openid = models.CharField(verbose_name='微信唯一ID', max_length=64, null=True, blank=True)
　　....
 

