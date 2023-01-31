import joblib


def test_train_model(app_client, test_auth, test_model_path, mocker):
    endpoint = "/wine/quality"
    url_params = """fixed_acidity=5&volatile_acidity=1&\
citric_acid=0.5&residual_sugar=3&\
chlorides=0.4&free_sulfur_dioxide=5&total_sulfur_dioxide=9&\
density=1&pH=3&sulphates=1&alcohol=12"""

    mocker.patch(
        "wine_predictor_api.services.predictor.estimate_wine_quality",
        return_value=joblib.load(test_model_path),
        autospec=True,
    )

    response = app_client.get(
        f"{endpoint}?{url_params}", headers={"Authorization": test_auth}
    )

    assert response.status_code == 200
