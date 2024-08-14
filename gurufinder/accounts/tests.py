from django.test import TestCase

# {% extends 'base.html' %}
# {% load static %}
# {% load ratings %}
#
# {% block content %}
#     <div class="container">
#         <h2 class="pt-5 pb-4">Tutors</h2>
#            <div class="border p-4" style="float:right;">
#                <h3>Our Sidebar</h3>
#                <p class="text-muted">Lorem ipsum dolor sit amet consectetur.</p>
#                <ul class="list-group">
#                    <li class="list-group-item list-group-item-light">Home</li>
#                    <li class="list-group-item list-group-item-light">Announcements</li>
#                    <li class="list-group-item list-group-item-light">Calendars</li>
#                    <li class="list-group-item list-group-item-light">etc</li>
#                </ul>
#            </div>
#         {% for tutor in tutors %}
#             {% if tutor.is_tutor and tutor.tutor_profile.is_validated %}
#                 <div class="border card box-shadow-hover mb-3" style="max-width: 900px; border-radius">
#                   <div class="row g-0">
#                     <div class="col-md-2">
#                       <img src="{{ tutor.image.url }}" class="article-img" alt="{{ tutor.first_name }}">
#                     </div>
#                     <div class="col-md-10">
#                       <div class="card-body">
#                         <h5 class="card-title"><a class="text-dark" href="{% url 'tutor_detail' tutor.id %}" style="text-decoration: none;">{{ tutor.first_name|capfirst }} {{ tutor.last_name|capfirst }}</a></h5>
#                         <h4 class="text-primary"><a href="{% url 'tutor_detail' tutor.id %}" style="text-decoration: none">{{ tutor.tutor_profile.profile_headline|capfirst }}</a></h4>
#                           {% if tutor.tutor_profile.profile_headline|add:tutor.tutor_profile.bio|length > 255 %}
#                             <h5 class="text-muted">{{ tutor.tutor_profile.bio|truncatechars:260 }}<a href="{% url 'tutor_detail' tutor.id %}" style="text-decoration: none;">read more</a></h5>
#                           {% else %}
#                             <h5 class="text-muted"><a href="{% url 'tutor_detail' tutor.id %}" style="text-decoration: none;">{{ tutor.tutor_profile.bio|capfirst }}</a></h5>
#                           {% endif %}
#                           {% ratings tutor %}
#                       </div>
#                     </div>
#                   </div>
#                 </div>
#             {% endif %}
#         {% endfor %}
#  <!-- pagination -->
#     {% if is_paginated  %}
#
#         {% if page_obj.has_previous %}
#             <a class="btn btn-outline-info mb-4" href="?page=1">First</a>
#             <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.previous_page_number }}">Previous</a>
#         {% endif %}
#
#         {% for num in page_obj.paginator.page_range %}
#             {% if page_obj.number == num %}
#                 <a class="btn btn-info mb-4" href="?page={{ num }}">{{ num }}</a>
#             {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
#                 <a class="btn btn-outline-info mb-4" href="?page={{ num }}">{{ num }}</a>
#             {% endif %}
#         {% endfor %}
#
#         {% if page_obj.has_next %}
#             <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.next_page_number }}">Next</a>
#             <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.paginator.num_pages }}">Last</a>
#         {% endif %}
#
#     {% endif %}
#     </div>
# {% endblock content %}





# <table id="class-time-table">
#                   <tr>
#                       <th></th>
#                       {% for slot in slots %}
#                       <th scope="row">{{slot.start_time}}</th>
#                       {% endfor %}
#                   </tr>
#                   <tr>
#                       <th>Monday</th>
#                       {%for slot in classrooms.classroom_slots.all%}
#                       {%if slot.day.id == 1 %}
#                       <td>{{slot.slot_subject}}</td>
#                       {% endif %}
#                       {% endfor %}
#                   </tr>
#                   <tr>
#                       <th>Tuesday</th>
#                       {%for slot in classrooms.classroom_slots.all%}
#                       {%if slot.day.id == 2 %}
#                       <td>{{slot.slot_subject}}</td>
#                       {% endif %}
#                       {% endfor %}
#                   </tr>
#                   <tr>
#                       <th>Wednesday</th>
#                       {%for slot in classrooms.classroom_slots.all%}
#                       {%if slot.day.id == 3 %}
#                       <td>{{slot.slot_subject}}</td>
#                       {% endif %}
#                       {% endfor %}
#                   </tr>
#                   <tr>
#                       <th>Thursday</th>
#                       {%for slot in classrooms.classroom_slots.all%}
#                       {%if slot.day.id == 4 %}
#                       <td>{{slot.slot_subject}}</td>
#                       {% endif %}
#                       {% endfor %}
#                   </tr>
#                   <tr>
#                       <th>Friday</th>
#                       {%for slot in classrooms.classroom_slots.all%}
#                       {%if slot.day.id == 5 %}
#                       <td>{{slot.slot_subject}}</td>
#                       {% endif %}
#                       {% endfor %}
#                   </tr>
#               </table>
#           </div>