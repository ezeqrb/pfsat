import pytest
from django.test import TestCase,Client
from django.contrib.auth.models import User
from paciente.models import Paciente, ObraSocial
from medico.models import Medico, Especialidad

class UsuarioTestCase(TestCase):
    def setUp(self):
        self.cliente = Client()
        self.user1 = User.objects.create(
            username = "juan.perez",
            email = "jperez@gmail.com",
            first_name = "Juan",
            last_name = "Perez",
            password = "123",
            is_staff = False
        )

        self.user2 = User.objects.create(
            username = "juana.perez",
            email = "juanaperez@gmail.com",
            first_name = "Juana",
            last_name = "Perez",
            password = "111",
            is_staff = False
        )

        self.superuser = User.objects.create(
            username = "juan.lopez",
            email = "jlopez@gmail.com",
            first_name = "Juan",
            last_name = "López",
            password = "321",
            is_staff = True,
            is_superuser = True
        )

        self.paciente = Paciente.objects.create(
            user = self.user1,
            dni = "23456789",
            fechaNacimiento = "1975-01-01",
            sexo = "m"
        )

        self.medico = Medico.objects.create(
            user = self.user2,
            dni = "20456789",
            fechaNacimiento = "1970-01-01",
            sexo = "f"
        )
    
    def test_create_user(self):
        self.assertEqual(self.user1.is_staff, False)
        self.assertEqual(self.user1.is_superuser, False)
        
        self.assertEqual(self.user2.is_staff, False)
        self.assertEqual(self.user2.is_superuser, False)

    def test_create_superuser(self):
        self.assertEqual(self.superuser.is_staff, True)
        self.assertEqual(self.superuser.is_superuser, True)

    def test_login_paciente(self):
        self.user1.set_password('123')
        self.user1.save()
        response = self.client.login(username='juan.perez',password='123')
        self.assertEqual(response, True)

    def test_login_paciente_fail(self):
        self.user1.set_password('123')
        self.user1.save()
        response = self.client.login(username='juana.perez',password='111')
        self.assertEqual(response, False)

    def test_list_usuarios(self):
        self.superuser.set_password('321')
        self.superuser.save()
        self.client.login(username='juan.lopez', password='321')
        response = self.client.get('/admin-list_usuarios')
        self.assertEqual(response.status_code, 200)

    def test_list_usuarios_fail(self):
        self.user2.set_password('111')
        self.user2.save()
        self.client.login(username='juana.perez', password='111')
        response = self.client.get('/admin-list_usuarios')
        self.assertEqual(response.status_code, 302)
    
'''
@pytest.fixture
def create_user():
    # creación de usuario
    return User(
        username = "juan.perez",
        email = "jperez@gmail.com",
        first_name = "Juan",
        last_name = "Perez",
        password = "123"
    )

@pytest.mark.django_db
def test_create_paciente(create_user):
    create_user.is_staff = False
    create_user.save()

    # creación de obra social
    obra_social = ObraSocial.objects.create(
        nombre = "OSDE"
    )
    assert obra_social.nombre == "OSDE"

    # creación de paciente
    paciente = Paciente.objects.create(
        user = create_user,
        obraSocial = obra_social,
        dni = "23456789",
        fechaNacimiento = "1975-01-01",
        sexo = "m"
    )
    assert paciente.dni == "23456789"

@pytest.mark.django_db
def test_create_medico(create_user):
    create_user.is_staff = False
    create_user.save()

    # creación de especialidad
    especialidad = Especialidad.objects.create(
        nombre = "Cardiólogo"
    )
    assert especialidad.nombre == "Cardiólogo"

    # creación de médico
    medico = Medico.objects.create(
        user = create_user,
        especialidad = especialidad,
        dni = "21234567",
        fechaNacimiento = "1971-01-01",
        sexo = "m"
    )
    assert medico.sexo == "m"

@pytest.mark.django_db
def test_create_admin(create_user):
    create_user.is_staff = True
    create_user.is_superuser = True
    create_user.save()

    assert create_user.is_staff
    assert create_user.is_superuser

@pytest.mark.django_db
def test_create_paciente_fail():
    with pytest.raises(Exception):  
        Paciente.objects.create(
            dni = "23456789",
            fechaNacimiento = "1975-01-01",
            sexo = "m"
        )

@pytest.mark.django_db
def test_create_medico_fail():
    with pytest.raises(Exception):  
        Medico.objects.create(
            dni = "21234567",
            fechaNacimiento = "1971-01-01",
            sexo = "m"
        )
'''
