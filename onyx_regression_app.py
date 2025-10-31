from nicegui import ui
import pickle
import pandas as pd

# Load models
def load_models():
    models = {}
    try:
        with open('simple.pkl', 'rb') as f:
            models['simple'] = pickle.load(f)
    except:
        models['simple'] = None
    
    try:
        with open('polynomial_transformer.pkl', 'rb') as f:
            models['poly_transformer'] = pickle.load(f)
        with open('linear_model.pkl', 'rb') as f:
            models['poly_lin_reg'] = pickle.load(f)
    except:
        models['poly_transformer'] = None
        models['poly_lin_reg'] = None
    
    try:
        with open('model.pkl', 'rb') as f:
            models['multiple'] = pickle.load(f)
    except:
        models['multiple'] = None
    
    return models

models = load_models()

# Main page
@ui.page('/')
def main_page():
    ui.colors(primary='#4CAF50')
    
    with ui.card().classes('absolute-center').style('width: 500px; padding: 30px; background-color: #f0f0f0'):
        ui.label('Linear Regression Predictor').classes('text-h4 text-weight-bold text-center').style('color: #333')
        ui.label('Select a regression type to make predictions').classes('text-subtitle1 text-center').style('color: #666; margin-bottom: 30px')
        
        ui.button('Simple Linear Regression\n(Study Hours → Marks)', 
                  on_click=lambda: ui.open('/simple')).classes('w-full').style(
            'height: 80px; background-color: #4CAF50; color: white; font-size: 14px; margin: 10px 0'
        )
        
        ui.button('Polynomial Regression\n(Level → Salary)', 
                  on_click=lambda: ui.open('/polynomial')).classes('w-full').style(
            'height: 80px; background-color: #2196F3; color: white; font-size: 14px; margin: 10px 0'
        )
        
        ui.button('Multiple Linear Regression\n(Startup Profit Prediction)', 
                  on_click=lambda: ui.open('/multiple')).classes('w-full').style(
            'height: 80px; background-color: #FF9800; color: white; font-size: 14px; margin: 10px 0'
        )
        
        ui.label('@ ONYX PYTHON 2ND APP | 2025').classes('text-caption text-center').style('color: #999; font-style: italic; margin-top: 30px')

# Simple Linear Regression page
@ui.page('/simple')
def simple_page():
    if models['simple'] is None:
        ui.notify('Error: simple.pkl model file not found!', type='negative')
        ui.open('/')
        return
    
    with ui.card().classes('absolute-center').style('width: 450px; padding: 30px; background-color: #f0f0f0'):
        ui.label('Predict Marks from Study Hours').classes('text-h5 text-weight-bold text-center')
        
        ui.space()
        
        with ui.row().classes('w-full items-center'):
            ui.label('Study Hours (1-10):').style('width: 150px')
            hours_input = ui.number(value=5, min=1, max=10, step=0.5).style('width: 150px')
        
        result_label = ui.label('').classes('text-h6 text-weight-bold text-center').style('color: #4CAF50; margin: 20px 0')
        
        def predict():
            try:
                hrs = hours_input.value
                if hrs >= 1 and hrs <= 10:
                    marks = models['simple'].predict([[hrs]])
                    result_label.text = f'Predicted Marks: {int(marks[0])}'
                    result_label.style('color: #4CAF50')
                else:
                    result_label.text = 'Please enter hours between 1 and 10'
                    result_label.style('color: #f44336')
            except Exception as e:
                result_label.text = f'Error: {str(e)}'
                result_label.style('color: #f44336')
        
        ui.button('Predict', on_click=predict).classes('w-full').style('background-color: #4CAF50; color: white; margin: 10px 0')
        ui.button('Back to Menu', on_click=lambda: ui.open('/')).classes('w-full').style('background-color: #757575; color: white')

# Polynomial Regression page
@ui.page('/polynomial')
def polynomial_page():
    if models['poly_transformer'] is None or models['poly_lin_reg'] is None:
        ui.notify('Error: polynomial model files not found!', type='negative')
        ui.open('/')
        return
    
    with ui.card().classes('absolute-center').style('width: 450px; padding: 30px; background-color: #f0f0f0'):
        ui.label('Predict Salary from Level').classes('text-h5 text-weight-bold text-center')
        
        ui.space()
        
        with ui.row().classes('w-full items-center'):
            ui.label('Level:').style('width: 150px')
            level_input = ui.number(value=5, min=1, max=10, step=1, format='%.0f').style('width: 150px')
        
        result_label = ui.label('').classes('text-h6 text-weight-bold text-center').style('color: #2196F3; margin: 20px 0')
        
        def predict():
            try:
                level = int(level_input.value)
                level_poly = models['poly_transformer'].transform([[level]])
                predict_sal = models['poly_lin_reg'].predict(level_poly)
                result_label.text = f'Predicted Salary: ${int(predict_sal[0]):,}'
                result_label.style('color: #2196F3')
            except Exception as e:
                result_label.text = f'Error: {str(e)}'
                result_label.style('color: #f44336')
        
        ui.button('Predict', on_click=predict).classes('w-full').style('background-color: #2196F3; color: white; margin: 10px 0')
        ui.button('Back to Menu', on_click=lambda: ui.open('/')).classes('w-full').style('background-color: #757575; color: white')

# Multiple Linear Regression page
@ui.page('/multiple')
def multiple_page():
    if models['multiple'] is None:
        ui.notify('Error: model.pkl model file not found!', type='negative')
        ui.open('/')
        return
    
    with ui.card().classes('absolute-center').style('width: 500px; padding: 30px; background-color: #f0f0f0'):
        ui.label('Startup Profit Prediction').classes('text-h5 text-weight-bold text-center')
        
        ui.space()
        
        with ui.column().classes('w-full'):
            with ui.row().classes('w-full items-center'):
                ui.label('California (0 or 1):').style('width: 180px; font-size: 13px')
                california_input = ui.number(value=0, min=0, max=1, step=1, format='%.0f').style('width: 150px')
            
            with ui.row().classes('w-full items-center'):
                ui.label('New York (0 or 1):').style('width: 180px; font-size: 13px')
                newyork_input = ui.number(value=0, min=0, max=1, step=1, format='%.0f').style('width: 150px')
            
            with ui.row().classes('w-full items-center'):
                ui.label('Florida (0 or 1):').style('width: 180px; font-size: 13px')
                florida_input = ui.number(value=0, min=0, max=1, step=1, format='%.0f').style('width: 150px')
            
            with ui.row().classes('w-full items-center'):
                ui.label('R&D Spend:').style('width: 180px; font-size: 13px')
                rd_input = ui.number(value=100000, min=0, step=1000, format='%.0f').style('width: 150px')
            
            with ui.row().classes('w-full items-center'):
                ui.label('Administration Spend:').style('width: 180px; font-size: 13px')
                admin_input = ui.number(value=100000, min=0, step=1000, format='%.0f').style('width: 150px')
            
            with ui.row().classes('w-full items-center'):
                ui.label('Marketing Spend:').style('width: 180px; font-size: 13px')
                marketing_input = ui.number(value=100000, min=0, step=1000, format='%.0f').style('width: 150px')
        
        result_label = ui.label('').classes('text-h6 text-weight-bold text-center').style('color: #FF9800; margin: 20px 0')
        
        def predict():
            try:
                california = int(california_input.value)
                newyork = int(newyork_input.value)
                florida = int(florida_input.value)
                rd = int(rd_input.value)
                admin = int(admin_input.value)
                marketing = int(marketing_input.value)
                
                if california not in [0, 1] or newyork not in [0, 1] or florida not in [0, 1]:
                    result_label.text = 'Location values must be 0 or 1'
                    result_label.style('color: #f44336')
                    return
                
                user_input = {
                    'california': california,
                    'newyork': newyork,
                    'florida': florida,
                    'rd': rd,
                    'admin': admin,
                    'marketing': marketing
                }
                
                user_data = pd.DataFrame(user_input, index=[0])
                prediction = models['multiple'].predict(user_data)
                
                result_label.text = f'Predicted Profit: ${int(prediction[0]):,}'
                result_label.style('color: #FF9800')
            except Exception as e:
                result_label.text = f'Error: {str(e)}'
                result_label.style('color: #f44336')
        
        ui.button('Predict', on_click=predict).classes('w-full').style('background-color: #FF9800; color: white; margin: 10px 0')
        ui.button('Back to Menu', on_click=lambda: ui.open('/')).classes('w-full').style('background-color: #757575; color: white')

ui.run(title='Linear Regression Predictor', port=8080)