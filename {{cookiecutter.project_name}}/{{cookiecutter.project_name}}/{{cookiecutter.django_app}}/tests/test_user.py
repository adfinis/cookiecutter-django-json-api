from django.urls import reverse
from rest_framework import status


def test_user_detail(client):
    url = reverse("userprofile-detail", args=[client.user.profile.id])

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert json["data"]["id"] == str(client.user.profile.id)
