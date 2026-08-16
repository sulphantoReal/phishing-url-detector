from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
import pandas as pd

FEATURE_COLS = ["url_length", "count_dots", "has_ip_address", "has_at_symbol",
                 "count_hyphens", "has_https", "count_slashes", "count_digits",
                 "has_suspicious_words"]


def load_data(filename):
    # split into X (features) and y (the actual label) like sklearn expects
    df = pd.read_csv(filename)
    X = df[FEATURE_COLS]
    y = df["status"]
    return df, X, y


def train_logistic_regression(X_train, X_test, y_train, y_test):
    # logistic regression needs scaled features or it barely converges -
    # learned this the hard way, kept getting ConvergenceWarning without it
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression()
    model.fit(X_train_scaled, y_train)
    predictions = model.predict(X_test_scaled)

    print("Logistic Regression Accuracy:", accuracy_score(y_test, predictions))
    print(confusion_matrix(y_test, predictions))
    return predictions


def train_random_forest(X_train, X_test, y_train, y_test):
    # tree models don't care about feature scale, so raw X_train/X_test is fine here
    rf_model = RandomForestClassifier(random_state=42)
    rf_model.fit(X_train, y_train)
    predictions = rf_model.predict(X_test)

    print("Random Forest Accuracy:", accuracy_score(y_test, predictions))
    print(confusion_matrix(y_test, predictions))
    return rf_model, predictions


def print_feature_importance(model, feature_cols):
    # which features the forest actually relied on - biggest first
    for name, importance in sorted(zip(feature_cols, model.feature_importances_),
                                    key=lambda x: x[1], reverse=True):
        print(name, importance)


def print_class_averages(df, feature_cols):
    # sanity check: do phishing vs legit URLs actually look different per feature?
    # (this is what showed has_https was backwards in this dataset)
    print(df.groupby("status")[feature_cols].mean())


if __name__ == "__main__":
    df, X, y = load_data("features_final.csv")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    train_logistic_regression(X_train, X_test, y_train, y_test)
    print_class_averages(df, FEATURE_COLS)

    rf_model, rf_predictions = train_random_forest(X_train, X_test, y_train, y_test)
    print_feature_importance(rf_model, FEATURE_COLS)
