from factorycps.control.supervisor import ResilientSupervisor

def test_safe_stop_on_critical_health():
    d=ResilientSupervisor().decide('NORMAL',False,1.0,.2,.9); assert d.state=='SAFE_STOP' and d.load_command==0
