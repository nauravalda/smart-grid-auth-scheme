from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

class SystemParameters:
    def __init__(self):
        self.__curve = ec.SECP256R1()  
        self.__pub = None  
        self.__priv = 0  

    @property
    def curve(self):
        return self.__curve

    @property
    def pub(self):
        return self.__pub

    @property
    def s(self):
        return self.__priv

    def init_parameters(self):
        # generate key pair
        private_key = ec.generate_private_key(self.__curve)
        public_key = private_key.public_key()
        self.__priv = private_key
        self.__pub = public_key

class SmartMeter:
    def __init__(self, sm_id, sp_id):
        self.sm_id = sm_id
        self.public_key = None
        self.sp_id = sp_id

    def generate_key_pair(self, curve):
        private_key = ec.generate_private_key(curve)
        self.public_key = private_key.public_key()
        return private_key

class ServiceProvider:
    def __init__(self, sp_id):
        self.sp_id = sp_id
        self.public_key = None

    def generate_key_pair(self, curve):
        private_key = ec.generate_private_key(curve)
        self.public_key = private_key.public_key()
        return private_key

class DataSMSP:
    def __init__(self):
        self.SM = []
        self.SP = []
    
    def regist_SM(self, sm_id):
        # choose avail sp_id
        print("Available SP:")
        for sp in self.SP:
            print(sp.sp_id)
        sp_id = input("Choose sp_id: ")

        sm = SmartMeter(sm_id, sp_id)
        priv = sm.generate_key_pair(params.curve)
        self.SM.append(sm)
        pub_sp = None
        for sp in self.SP:
            if sp.sp_id == sp_id:
                pub_sp = sp.public_key
                break

        return priv, pub_sp

    def regist_SP(self, sp_id):
        sp = ServiceProvider(sp_id)
        priv = sp.generate_key_pair(params.curve)
        self.SP.append(sp)
        return priv

params = SystemParameters()
data = DataSMSP()

# def init():
#     params.init_parameters()

# init()







        

    




if __name__ == '__main__':
    system_params = SystemParameters()

    system_params.init_parameters()


    print("Curve:", system_params.curve)
    print("Public Key:", system_params.pub)
    print("Private Key:", system_params.s)
    try:
        print(system_params._priv)
    except AttributeError:
        print("_priv is private and cannot be accessed from outside the class")


    try:
        system_params.curve = ec.SECP384R1()
        system_params.pub = "new_public_key"
    except AttributeError:
        print("Curve and Public Key are private and cannot be updated from outside the class")


