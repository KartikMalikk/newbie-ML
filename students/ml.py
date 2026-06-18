import pandas as pd
from sklearn.linear_model import LinearRegression
from .models import Student

def train_and_predict():
    qs = Student.objects.exclude(marks__isnull=True)
    if qs.count() < 5:
        return
    
    df = pd.DataFrame(list(qs.values()))

    X = df[['hours_studied', 'attendance', 'previous_score']]
    y = df['marks']

    model = LinearRegression()
    model.fit(X, y)
    
    missing = Student.objects.filter(marks__isnull=True)
    for s in missing:
        df_input = pd.DataFrame(
            [[s.hours_studied, s.attendance, s.previous_score]],
            columns=['hours_studied', 'attendance', 'previous_score']
        )
        prediction = model.predict(df_input)
        score = prediction.item()  # extract scalar value
        s.marks = round(score, 2)
        s.save()
