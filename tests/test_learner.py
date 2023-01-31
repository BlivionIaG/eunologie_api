from pandas import read_csv
import joblib


def test_train_model(
    app_client,
    test_auth,
    test_data_path,
    test_model_path,
    mocker
):
    endpoint = "/wine/model"

    mocker.patch(
        "wine_predictor_api.services.learner.load_data",
        return_value=read_csv(test_data_path),
        autospec=True,
    )

    mocker.patch(
        "wine_predictor_api.services.learner.load_model",
        return_value=joblib.load(test_model_path),
        autospec=True,
    )

    mocker.patch(
        "wine_predictor_api.services.learner.save_model",
        return_value=None,
        autospec=True,
    )

    response = app_client.patch(endpoint, headers={"Authorization": test_auth})

    assert response.status_code in [200, 201]
