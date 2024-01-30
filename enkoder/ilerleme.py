import pickle
import sklearn 
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

def predict_ileri(aci,enkoder,modelLinear,modelPoly):
    pre = [[aci,enkoder]]
    predict_ilerleme = modelLinear.predict(modelPoly.transform(pre))
    return predict_ilerleme

    
def predict_yonlendirme(aci,enkoder,modelLinear,modelPoly):
    pre = [[aci,enkoder]]
    predict_yonlenme = modelLinear.predict(modelPoly.transform(pre))
    return predict_yonlendirme


"""
model_ileri_linear = pickle.load(open("ilerlemeLinear.pickle","rb"))
model_ileri_poly = pickle.load(open("ilerlemePoly.pickle","rb"))
a = predict_ileri(-98.0,278,model_ileri_linear,model_ileri_poly)
print(a)"""