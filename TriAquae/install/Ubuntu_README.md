
��װ��������
sudo apt-get install gcc make sysstat nc
sudo apt-get install python-dev
sudo apt-get install snmpd
sudo apt-get install mysql-client mysql-server
sudo /etc/init.d/mysql start


��װrrdtool
sudo apt-get install rrdtool


��װTriAquae
sudo tar zxf TriAquae.tar.gz
cd TriAquae/install
sudo python setup.py build --prefix=/opt/soft/TriAquae
sudo python setup.py install

�޸����ݿ��IP
�޸�tri_config�����ļ�
MySQL_Name = 'TriAquae'
MySQL_User = 'root'
MySQL_Pass = 'coral'
Tri_IP = '192.168.2.2'
���ñ��������ʼ�
SMTP_server = 'smtp.126.com'
Mail_username = 'mailuser'
Mail_password = 'mailpass'

��ʼ��
sudo python setup.py init

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