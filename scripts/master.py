import sys, os, pwd, signal, time, shutil
from subprocess import *
from resource_management import *

class MarketBasket(Script):
  def install(self, env):
    self.configure(env)
    import params
    
    if not os.path.exists(params.install_dir): 
        os.makedirs(params.install_dir)
    os.chdir(params.install_dir)
    Execute('yum install -y git')
    Execute('git clone ' + params.download_url)
    Execute('cd SE-demo/Retail/RetailAnalytics')
    Execute('unzip OnlineRetail.txt.zip')
    Execute('OnlineRetail.txt /tmp/')
    Execute('sudo -u hdfs hadoop fs -mkdir /user/root')
    Execute('sudo -u hdfs hadoop fs -mkdir /user/root/retail')
    Execute('sudo -u hdfs hadoop fs -mkdir /user/root/retail/retailsalesraw')
    Execute('sudo -u hdfs hadoop fs -chown -R root /user/root')
    Execute('sudo -u hdfs hadoop fs -put /tmp/OnlineRetail.txt /user/root/retail/retailsalesraw')


  def pig(self, env):
    self.configure(env)
    import params
    Execute('pig RetailSalesIngestion.pig')
    Execute('pig MBADataPrep.pig')

    
  def hive(self, env):
    self.configure(env)
    import params
    Execute('cp RetailSalesRaw.ddl RetailSalesRaw.sql')
    Execute('cp RetailSales.ddl RetailSales.sql')
    Execute('hive -f RetailSalesRaw.sql')
    Execute('hive -f RetailSales.sql')

  def configure(self, env):
    import params
    env.set_params(params)

if __name__ == "__main__":
  MarketBasket().execute()