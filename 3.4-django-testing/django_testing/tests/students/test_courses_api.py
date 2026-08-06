import pytest
from django.urls import reverse
from rest_framework import status

from students.models import Course


@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    """Проверка получения первого курса (retrieve-логика)."""
    course = course_factory()
    url = reverse("courses-detail", kwargs={"pk": course.id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == course.id
    assert response.json()["name"] == course.name


@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    """Проверка получения списка курсов (list-логика)."""
    course1 = course_factory(name="Math")
    course2 = course_factory(name="Physics")
    url = reverse("courses-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    ids = {item["id"] for item in data}
    assert {course1.id, course2.id} <= ids


@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    """Проверка фильтрации списка курсов по id."""
    course1 = course_factory(name="Math")
    course2 = course_factory(name="Physics")
    url = reverse("courses-list")
    response = api_client.get(url, data={"id": [course1.id]})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == course1.id


@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    """Проверка фильтрации списка курсов по name."""
    course1 = course_factory(name="Math")
    course2 = course_factory(name="Physics")
    course3 = course_factory(name="Mathematics")
    url = reverse("courses-list")
    response = api_client.get(url, data={"name": "Math"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == course1.id


@pytest.mark.django_db
def test_create_course(api_client):
    """Тест успешного создания курса."""
    url = reverse("courses-list")
    data = {"name": "Chemistry"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Course.objects.filter(name="Chemistry").exists()


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    """Тест успешного обновления курса."""
    course = course_factory(name="Biology")
    url = reverse("courses-detail", kwargs={"pk": course.id})
    data = {"name": "Biology Advanced"}
    response = api_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    course.refresh_from_db()
    assert course.name == "Biology Advanced"


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    """Тест успешного удаления курса."""
    course = course_factory(name="History")
    url = reverse("courses-detail", kwargs={"pk": course.id})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Course.objects.filter(id=course.id).exists()
