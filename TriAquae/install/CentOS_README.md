

��װ��������
yum install gcc gcc-c++ make sysstat nc -y
yum install python-devel -y
yum install net-snmp net-snmp-utils net-snmp-devel -y
yum install mysql mysql-server mysql-devel -y
/etc/init.d/mysqld start


��װrrdtool
yum install cairo-devel libxml2-devel pango-devel pango libpng-devel freetype freetype-devel libart_lgpl libart_lgpl-devel intltool -y
yum install rrdtool rrdtool-devel -y


����pythonΪ2.7����
python -V
sh install/python_ins27.sh
python -V
˵����5.xϵͳpythonĬ�ϰ汾��2.4����װ�����Դ�����python 2.7�Ľű�,��װ��ɺ��ڴμ��python�汾


��װTriAquae
tar zxf TriAquae.tar.gz
cd TriAquae/install
python setup.py build --prefix=/opt/soft/TriAquae
python setup.py install

�޸����ݿ��IP
�޸�tri_config�����ļ�
MySQL_Name = 'TriAquae'
MySQL_User = 'root'
MySQL_Pass = 'coral'
Tri_IP = '192.168.2.2'
���ñ��������ʼ�
SMTP_server = 'smtp.company.com' #replace it to your company smtp server
Mail_username = 'mailuser'
Mail_password = 'mailpass'


��ʼ��
python setup.py init


����TriAquae
cd /your installdir/TriAquae/sbin
python tri_service.py start
˵��������Ĭ��Ϊ7000�˿�


��½TriAquae
http://ip:7000/
Ĭ���˻���admin
Ĭ�����룺triaquae
ע�⣺�ر�iptables


FAQ
1������tri_service.pyʱ���������
ImportError: libpython2.7.so.1.0: cannot open shared object file: No such file or directory
���������
  ����Ϊpython2.7

2����½���ݻ�����Զ�̷���������ʾ������Ϣ�����κ����
���������
  logsĿ¼��Ҫ777Ȩ��




