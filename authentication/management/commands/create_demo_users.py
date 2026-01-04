from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    help = 'Creates demo users for testing'

    def handle(self, *args, **kwargs):
        # Create groups if they don't exist
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        pm_group, _ = Group.objects.get_or_create(name='Project Manager')
        dev_group, _ = Group.objects.get_or_create(name='Developer')
        submitter_group, _ = Group.objects.get_or_create(name='Submitter')

        demo_users = [
            {'username': 'demo_admin', 'email': 'admin@demo.com', 'first_name': 'Admin', 'last_name': 'User', 'group': admin_group, 'is_staff': True, 'is_superuser': True},
            {'username': 'demo_project_manager', 'email': 'pm@demo.com', 'first_name': 'Project', 'last_name': 'Manager', 'group': pm_group},
            {'username': 'demo_developer', 'email': 'dev@demo.com', 'first_name': 'Dev', 'last_name': 'User', 'group': dev_group},
            {'username': 'demo_submitter', 'email': 'submitter@demo.com', 'first_name': 'Submit', 'last_name': 'User', 'group': submitter_group},
        ]

        password = 'pooping123'

        for user_data in demo_users:
            username = user_data['username']
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'User {username} already exists'))
                continue

            user = User.objects.create_user(
                username=username,
                email=user_data['email'],
                password=password,
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )

            if user_data.get('is_staff'):
                user.is_staff = True
                user.save()

            if user_data.get('is_superuser'):
                user.is_superuser = True
                user.save()

            user.groups.add(user_data['group'])
            self.stdout.write(self.style.SUCCESS(f'Successfully created demo user: {username}'))

        self.stdout.write(self.style.SUCCESS('\nDemo users created with password: pooping123'))
