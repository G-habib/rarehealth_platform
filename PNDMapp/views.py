import os 
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tensorflow import keras
from keras.models import load_model
from base.models import Prediction, Patient
import joblib
model_path = r'C:\Users\HP 2018\Desktop\New folder (2)\hb\proj\savedModels\PNDM_disease_DL_prediction_v2.h5'
model = load_model(model_path)

# Create your views here.
@login_required(login_url='login')
def predictor(request):
    return render(request, 'index.html')
@login_required(login_url='login')
def formInfo(request):

    age = request.POST.get('age')
    HbA1c = request.POST.get('HbA1c')
    Birth_Weight = request.POST.get('Birth_Weight')
    Insulin_level = request.POST.get('Insulin_level')
    Family_History = request.POST.get('Family_History')
    Developmental_Delay = request.POST.get('Developmental_Delay')
    # Convert Yes/No to 0/1
    if Family_History == 'Yes':
        Family_History_No = '0'
        Family_History_Yes = '1'
    else:
        Family_History_No = '1'
        Family_History_Yes = '0'

    if Developmental_Delay == 'Yes':
        Developmental_Delay_No = '0'
        Developmental_Delay_Yes = '1'
    else:
        Developmental_Delay_No = '1'
        Developmental_Delay_Yes = '0'


    # prediction
    input_data = [float(age), float(HbA1c), float(Birth_Weight), float(Insulin_level), int(Family_History_No), int(Family_History_Yes), int(Developmental_Delay_No), int(Developmental_Delay_Yes)]
    print(input_data)
    # change the input_data to a numpy array
    import numpy as np
    #input_data_as_numpy_array = np.asarray(input_data)
    input_data_np = np.array([input_data])
    print(input_data_np)

    # Load the scaler
    scaler_path = r'C:\Users\HP 2018\Desktop\New folder (2)\hb\proj\savedModels\scaler.pkl'
    scaler = joblib.load(scaler_path)
    scaler.feature_names_in_ = None
    input_data_std = scaler.transform(input_data_np)
    print(input_data_std)

    y_predct = model.predict(input_data_std)
    print(y_predct)

    y_pred_label = [np.argmax(y_predct)]
    print(y_pred_label)

    if (y_pred_label[0] == 0):
        y_pred = 'do not have PNDM'
    else:
        y_pred = 'have PNDM'

    # Save prediction result to database
    patient = None
    if hasattr(request.user, 'patient'):
        patient = request.user.patient

    prediction = Prediction(
        patient=patient,
        age=float(age),
        HbA1c=float(HbA1c),
        birth_weight=float(Birth_Weight),
        insulin_level=float(Insulin_level),
        family_history=Family_History,
        developmental_delay=Developmental_Delay,
        result=y_pred
    )
    prediction.save()

    return render(request, 'result.html', {'result': y_pred})

