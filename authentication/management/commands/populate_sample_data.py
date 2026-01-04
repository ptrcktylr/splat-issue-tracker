from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from projects.models import Project
from tickets.models import Ticket, Comment
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populates database with sample projects and tickets'

    def handle(self, *args, **kwargs):
        # Get demo users
        try:
            admin = User.objects.get(username='demo_admin')
            pm = User.objects.get(username='demo_project_manager')
            dev = User.objects.get(username='demo_developer')
            submitter = User.objects.get(username='demo_submitter')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Demo users not found! Run create_demo_users first'))
            return

        # Sample projects
        projects_data = [
            {
                'name': 'E-Commerce Platform',
                'description': 'Main customer-facing e-commerce website with shopping cart, checkout, and user accounts.',
                'assigned_users': [pm, dev],
            },
            {
                'name': 'Mobile App - iOS',
                'description': 'Native iOS application for browsing products and placing orders on the go.',
                'assigned_users': [pm, dev],
            },
            {
                'name': 'Admin Dashboard',
                'description': 'Internal dashboard for managing inventory, orders, and customer data.',
                'assigned_users': [dev],
            },
            {
                'name': 'Payment Gateway Integration',
                'description': 'Secure payment processing system integrating with multiple payment providers.',
                'assigned_users': [pm, dev],
            },
            {
                'name': 'Customer Support Portal',
                'description': 'Help desk and ticket management system for customer support team.',
                'assigned_users': [dev],
            },
        ]

        # Sample tickets data
        tickets_data = [
            # E-Commerce Platform tickets
            ('Shopping cart not updating quantity', 'bug', 'major', 'fixed', 'When clicking the + button on cart items, the quantity doesn\'t update immediately. User needs to refresh the page.'),
            ('Add wishlist functionality', 'feature request', 'medium', 'assigned', 'Users want to save products to a wishlist for later purchase.'),
            ('Checkout page timeout', 'bug', 'critical', 'accepted', 'Checkout page times out after 30 seconds on slow connections, losing all cart data.'),
            ('Implement search autocomplete', 'feature request', 'minor', 'new', 'Add autocomplete suggestions when users type in the search bar.'),
            ('Product images not loading', 'bug', 'major', 'fixed (verified)', 'Product images return 404 errors on product detail pages.'),

            # Mobile App tickets
            ('App crashes on iOS 18', 'bug', 'critical', 'assigned', 'Application crashes immediately on launch for iOS 18 users.'),
            ('Push notifications for order updates', 'feature request', 'medium', 'new', 'Send push notifications when order status changes.'),
            ('Improve app loading time', 'internal cleanup', 'medium', 'accepted', 'App takes 5+ seconds to load on first launch.'),

            # Admin Dashboard tickets
            ('Export orders to CSV', 'feature request', 'minor', 'fixed', 'Need ability to export order history to CSV format.'),
            ('Dashboard charts not responsive', 'bug', 'minor', 'new', 'Charts on dashboard don\'t resize properly on smaller screens.'),
            ('Add bulk user management', 'feature request', 'medium', 'new', 'Need to manage multiple users at once (delete, update roles, etc).'),

            # Payment Gateway tickets
            ('Payment failing for international cards', 'bug', 'critical', 'assigned', 'Customers with international credit cards getting payment declined errors.'),
            ('Security vulnerability in token storage', 'vulnerability', 'critical', 'fixed (verified)', 'Payment tokens stored in localStorage instead of secure httpOnly cookies.'),
            ('Add Apple Pay support', 'feature request', 'medium', 'new', 'Support Apple Pay as a payment method.'),

            # Customer Support Portal tickets
            ('Email notifications not sending', 'bug', 'major', 'assigned', 'Support ticket email notifications stopped working after last deployment.'),
            ('Add canned responses', 'feature request', 'minor', 'new', 'Support agents want templates for common responses.'),
        ]

        created_projects = []

        # Create projects
        for proj_data in projects_data:
            if not Project.objects.filter(name=proj_data['name']).exists():
                project = Project.objects.create(
                    name=proj_data['name'],
                    description=proj_data['description'],
                    created_by=admin
                )
                project.assigned_users.set(proj_data['assigned_users'])
                created_projects.append(project)
                self.stdout.write(self.style.SUCCESS(f'Created project: {project.name}'))

        # Assign tickets to projects
        project_ticket_counts = [5, 3, 3, 3, 2]  # tickets per project
        ticket_idx = 0

        for i, project in enumerate(created_projects):
            num_tickets = project_ticket_counts[i]

            for j in range(num_tickets):
                if ticket_idx >= len(tickets_data):
                    break

                title, ticket_type, priority, status, description = tickets_data[ticket_idx]

                # Assign ticket to appropriate user based on status
                assigned_to = None
                submitted_by = submitter

                if status in ['assigned', 'accepted', 'fixed', 'fixed (verified)']:
                    assigned_to = dev

                if not Ticket.objects.filter(title=title, project=project).exists():
                    ticket = Ticket.objects.create(
                        title=title,
                        description=description,
                        type=ticket_type,
                        priority=priority,
                        status=status,
                        assigned_to=assigned_to,
                        submitted_by=submitted_by,
                        project=project
                    )

                    # Add some comments to tickets
                    if random.choice([True, False]):
                        Comment.objects.create(
                            ticket=ticket,
                            author=dev if assigned_to else pm,
                            content=random.choice([
                                'I\'m looking into this issue now.',
                                'Can you provide more details about when this occurs?',
                                'This should be fixed in the next release.',
                                'I\'ve reproduced the issue and working on a fix.',
                                'This is a duplicate of another ticket, marking as such.',
                            ])
                        )

                    self.stdout.write(self.style.SUCCESS(f'  Created ticket: {title}'))

                ticket_idx += 1

        self.stdout.write(self.style.SUCCESS(f'\n✅ Sample data created successfully!'))
        self.stdout.write(self.style.SUCCESS(f'   {len(created_projects)} projects'))
        self.stdout.write(self.style.SUCCESS(f'   ~{ticket_idx} tickets with comments'))
