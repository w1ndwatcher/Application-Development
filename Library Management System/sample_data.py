from main import app
from werkzeug.security import generate_password_hash
from application.models import db, Section, EBook, IssueReturn, Ratings
from application.sec import datastore
from datetime import datetime

with app.app_context():
    db.create_all()
    datastore.find_or_create_role(name='librarian', description="Admin")
    datastore.find_or_create_role(name='general_user', description="General User")
    db.session.commit()

    if not datastore.find_user(email="librarian@library.com"):
        datastore.create_user(email="librarian@library.com", username="librarian@123", full_name="Ayushi Saxena", password=generate_password_hash('123456'), roles=['librarian'],active=True)
        db.session.commit()
    if not datastore.find_user(email="user1@library.com"):
        datastore.create_user(email="user1@library.com", username="user1@123", full_name="Bloom", password=generate_password_hash('123456789'), roles=['general_user'],active=True)
        db.session.commit()
    if not datastore.find_user(email="user2@library.com"):
        datastore.create_user(email="user2@library.com", username="user2@123", full_name="Stella", password=generate_password_hash('123456789'), roles=['general_user'],active=True)
        db.session.commit()
    if not datastore.find_user(email="user3@library.com"):
        datastore.create_user(email="user3@library.com", username="user3@123", full_name="Brandon", password=generate_password_hash('123456789'), roles=['general_user'],active=True)
        db.session.commit()
    if not datastore.find_user(email="user4@library.com"):
        datastore.create_user(email="user4@library.com", username="user4@123", full_name="Raven", password=generate_password_hash('123456789'), roles=['general_user'],active=True)
        db.session.commit()
    if not datastore.find_user(email="user5@library.com"):
        datastore.create_user(email="user5@library.com", username="user5@123", full_name="Ayesha", password=generate_password_hash('123456789'), roles=['general_user'],active=True)
        db.session.commit()
    
    sections = [Section(section_name = "History", section_icon = "fas fa-landmark", description = "Historical Books and Journals", created_by = "librarian@123"),
                Section(section_name = "Medicine", section_icon = "fas fa-pills", description = "Medical Papers and Journals", created_by = "librarian@123"),
                Section(section_name = "Coding", section_icon = "fas fa-laptop-code", description = "Programming Books", created_by = "librarian@123"),
                Section(section_name = "Physics", section_icon = "fas fa-magnet", description = "Physics Journals and Textbooks", created_by = "librarian@123"),
                Section(section_name = "Sports", section_icon = "fas fa-volleyball-ball", description = "Rule Books and Guides", created_by = "librarian@123"),
                Section(section_name = "Mathematics", section_icon = "fa fa-plus", description = "Textbooks and Log Tables", created_by = "librarian@123")]
    for section in sections:
        if not Section.query.filter_by(section_name = section.section_name).first():
            db.session.add(section)
            db.session.commit()
    
    
    book1 = '''The history of the ancient world spans thousands of years and covers the rise and fall of numerous civilizations, each contributing uniquely to human development. It begins with the advent of writing and recorded history around 3000 BCE in Mesopotamia, often hailed as the cradle of civilization. Here, the Sumerians developed the earliest known form of writing, cuneiform, which laid the foundation for record-keeping, literature, and complex administration. Concurrently, ancient Egypt flourished along the Nile River, known for its remarkable achievements in architecture, mathematics, and medicine, epitomized by the construction of the pyramids and the grandeur of pharaonic rule.

Further east, the Indus Valley Civilization emerged around 2600 BCE, notable for its advanced urban planning, sophisticated drainage systems, and enigmatic script. In China, the Xia, Shang, and Zhou dynasties laid the groundwork for Chinese culture, philosophy, and governance, introducing innovations such as oracle bones and bronze metallurgy.

The ancient world also witnessed the rise of the Greek and Roman civilizations, whose legacies profoundly shaped Western culture, politics, and thought. Classical Greece, with its city-states like Athens and Sparta, fostered advancements in philosophy, drama, and democracy. Rome, initially a small city-state, expanded to create one of the largest empires in history, influencing law, engineering, and military strategy.

In the Americas, civilizations such as the Olmec, Maya, and Aztec in Mesoamerica, and the Inca in South America, developed complex societies with impressive achievements in agriculture, architecture, and astronomy.

The ancient world was a tapestry of interconnected cultures, driven by trade, conquest, and the exchange of ideas. From the Persian Empire's vast network of roads and postal systems to the spread of Buddhism from India to East Asia, these interactions facilitated cultural diffusion and the spread of technologies, religions, and philosophies that shaped the course of human history. The legacies of these ancient civilizations continue to resonate, influencing modern society in countless ways, from our legal systems and architectural styles to philosophical and scientific thought.'''
    
    book2 = '''Why did certain societies develop advanced technology and political organization, while others remained hunter-gatherers? Diamond rejects the notion of racial superiority and instead argues that environmental factors played the decisive role in determining the distribution of wealth and power among human societies.

Diamond begins his analysis with the "Great Leap Forward," the period around 11,000 BCE when humans began to shift from hunting and gathering to agriculture. He argues that the availability of domesticable plants and animals gave certain societies, particularly those in the Fertile Crescent, a significant advantage. Agriculture allowed for food surpluses, which in turn supported population growth, urbanization, and specialization of labor. This set the stage for technological innovation and complex political structures.

Geography, according to Diamond, was a crucial determinant of a society’s development. The east-west axis of Eurasia facilitated the spread of crops, animals, and technologies, whereas the north-south orientation of Africa and the Americas posed significant ecological barriers. This meant that societies in Eurasia had a larger pool of resources and innovations to draw from, accelerating their development.

One of Diamond’s key arguments is the impact of germs on the fates of societies. The domestication of animals in Eurasia led to the transfer of diseases from animals to humans. Over time, Eurasians developed immunities to these diseases. When Europeans began to explore and conquer other parts of the world, their germs devastated indigenous populations who had no previous exposure or immunity. This "accidental" biological warfare was a decisive factor in the European conquests of the Americas and other regions.

Diamond also explores the role of technology, epitomized by guns and steel. He contends that technological advances were not solely the result of individual genius but were instead the cumulative result of centuries of innovation made possible by a society’s size and interconnectedness. Large, dense populations fostered more rapid technological and political developments. Steel weapons and firearms gave Eurasians a significant military advantage over the societies they encountered during their expansions.

Another significant theme in "Guns, Germs, and Steel" is the development of writing and centralized political organizations. Diamond argues that writing systems enabled the efficient administration of large states and empires, facilitating the coordination of complex societies and the dissemination of knowledge. Centralized governments could organize large-scale projects, maintain standing armies, and impose order over vast territories.

Diamond’s work has been both influential and controversial. Critics argue that he underemphasizes the role of human agency and cultural factors in shaping history. They also point out that some of his environmental determinism can be overly simplistic. Nevertheless, "Guns, Germs, and Steel" has significantly contributed to the understanding of global history by highlighting the profound impact of environmental factors and challenging ethnocentric explanations of global inequality.'''
    
    book3 = '''Agile software development is a methodology that has revolutionized the way software is designed, developed, and delivered. Born out of the need for a more flexible and collaborative approach to software development, Agile focuses on iterative progress, stakeholder involvement, and adaptability to changing requirements. Its origins trace back to the early 2000s when a group of software developers, frustrated with the inefficiencies of traditional development methods, formulated the Agile Manifesto, a set of guiding principles that emphasize individuals and interactions, working software, customer collaboration, and responding to change.

At the heart of Agile is the concept of iterative development. Unlike traditional waterfall models, which follow a linear and sequential approach, Agile breaks down the development process into small, manageable units called iterations or sprints. Each sprint typically lasts two to four weeks and involves cross-functional teams working on delivering a potentially shippable product increment. This iterative cycle allows teams to incorporate feedback, adapt to new requirements, and continuously improve the product throughout its development.

A key tenet of Agile is collaboration. Agile methodologies promote close cooperation between developers, customers, and other stakeholders. Daily stand-up meetings, often called scrums in Scrum methodology, ensure that team members are aligned, obstacles are identified early, and progress is continuously tracked. This transparency fosters a collaborative environment where feedback is valued and swiftly acted upon, ensuring that the final product meets the user's needs and expectations.

Agile’s adaptability is another cornerstone of its effectiveness. In a rapidly changing business environment, requirements often evolve. Agile methodologies embrace this reality by allowing and even encouraging changes throughout the development process. Instead of viewing changes as disruptions, Agile treats them as opportunities to deliver more value. This adaptability is facilitated by regular review sessions and retrospective meetings where teams reflect on what went well and what could be improved, making adjustments in real-time.

Various frameworks and methodologies fall under the Agile umbrella, each with its own unique practices and focus areas. Scrum, for example, emphasizes roles such as the Scrum Master and Product Owner, along with events like sprints, sprint planning, and sprint reviews. Kanban, another Agile methodology, focuses on visualizing the workflow, limiting work in progress, and optimizing flow. Extreme Programming (XP) emphasizes technical practices such as pair programming, test-driven development, and continuous integration.

Agile software development has had a profound impact on the industry. By prioritizing customer satisfaction, delivering functional software quickly, and fostering a culture of collaboration and continuous improvement, Agile has enabled teams to be more responsive and innovative. Companies that adopt Agile methodologies often experience faster time-to-market, higher quality products, and increased customer satisfaction.

However, Agile is not without its challenges. Implementing Agile requires a cultural shift within organizations, as it demands a high level of commitment, trust, and open communication. Teams must be empowered to make decisions, and management must be willing to embrace change and uncertainty. Additionally, Agile practices may need to be tailored to fit the specific context and needs of an organization, as a one-size-fits-all approach rarely works.

In conclusion, Agile software development represents a significant departure from traditional methodologies, offering a more flexible, collaborative, and adaptive approach to software creation. By focusing on iterative progress, stakeholder involvement, and responsiveness to change, Agile has transformed the software industry, enabling teams to deliver high-quality products that meet the evolving needs of users. While it presents certain challenges, the benefits of Agile make it a compelling choice for organizations seeking to thrive in today’s dynamic and fast-paced environment.'''
    
    
    book4 = '''Cancer is one of the most formidable diseases facing humanity today, characterized by the uncontrolled growth and spread of abnormal cells in the body. It is not a single disease but a complex group of over 100 different types, each with its own unique characteristics, behaviors, and treatments. Despite significant advances in medical research and treatment, cancer remains a leading cause of death worldwide, highlighting the need for continued research, awareness, and innovative treatment strategies.

The origins of cancer can be traced to genetic mutations that disrupt the normal regulatory mechanisms controlling cell growth and division. These mutations can be inherited, caused by environmental factors such as tobacco smoke, radiation, and carcinogens, or result from random errors during cell replication. Once these mutations accumulate, they can lead to the formation of a tumor, which can be benign (non-cancerous) or malignant (cancerous). Malignant tumors have the ability to invade surrounding tissues and spread to distant parts of the body through the bloodstream or lymphatic system in a process known as metastasis.

The symptoms and progression of cancer vary widely depending on the type and location of the disease. Common symptoms may include unusual lumps, unexplained weight loss, persistent pain, fatigue, and changes in skin appearance. Early detection through screening methods such as mammograms, colonoscopies, and Pap smears is crucial for improving survival rates, as it allows for treatment to begin before the cancer has advanced or spread.

Treatment options for cancer are diverse and depend on the type, stage, and location of the disease, as well as the patient's overall health and preferences. Traditional treatments include surgery to remove tumors, radiation therapy to destroy cancer cells, and chemotherapy to target rapidly dividing cells. These methods can be highly effective but often come with significant side effects, as they can also damage healthy cells.

In recent years, advances in medical research have led to the development of more targeted and less invasive treatments. Immunotherapy, which harnesses the body's immune system to fight cancer, has shown promise in treating certain types of cancer that were previously resistant to conventional treatments. Targeted therapies, which specifically target the molecular changes driving cancer growth, offer the potential for more precise and effective treatment with fewer side effects. Additionally, advances in genomics and personalized medicine are paving the way for treatments tailored to the genetic profile of an individual's cancer, potentially improving outcomes and reducing the likelihood of recurrence.

Despite these advancements, cancer remains a significant global health challenge. According to the World Health Organization (WHO), cancer is responsible for approximately one in six deaths worldwide, with an estimated 19.3 million new cases and 10 million deaths in 2020 alone. The burden of cancer is expected to increase in the coming decades due to population growth and aging, as well as lifestyle factors such as smoking, poor diet, and physical inactivity.

Efforts to combat cancer extend beyond medical treatment and research. Public health initiatives aimed at reducing risk factors, promoting early detection, and improving access to care are essential components of a comprehensive cancer control strategy. Education and awareness campaigns play a crucial role in encouraging healthy behaviors, such as avoiding tobacco and excessive sun exposure, maintaining a healthy weight, and getting regular screenings.

Support for cancer patients and their families is also a critical aspect of addressing the impact of the disease. Emotional and psychological support, financial assistance, and access to palliative care services can significantly improve the quality of life for those affected by cancer.

Cancer is a complex and multifaceted disease that poses a significant challenge to global health. While considerable progress has been made in understanding and treating cancer, continued research, innovation, and public health efforts are essential to reduce its prevalence and impact. By fostering collaboration across scientific, medical, and community spheres, we can work towards a future where cancer is a more manageable and less devastating disease.'''
    
    book5 = '''Internal medicine is a crucial field within the medical profession, focusing on the comprehensive care of adults through a detailed understanding of their various systems, diseases, and the intricate interplay between them. Internists, or internal medicine physicians, are trained to diagnose, treat, and prevent a wide range of illnesses, providing holistic and long-term care for patients. Their expertise extends across multiple organ systems and encompasses a variety of settings, from hospitals to outpatient clinics.

The roots of internal medicine can be traced back to ancient civilizations, where early physicians like Hippocrates and Galen laid the foundations for clinical observation and diagnosis. However, it was during the late 19th and early 20th centuries that internal medicine began to emerge as a distinct specialty. Advances in medical science, such as the development of bacteriology and the discovery of antibiotics, revolutionized the understanding and treatment of diseases, paving the way for the establishment of internal medicine as a cornerstone of modern healthcare.

Internists are often seen as the primary point of contact for patients navigating the complexities of adult health. Their role involves a broad range of responsibilities, including the management of chronic conditions like diabetes, hypertension, and heart disease, as well as acute illnesses such as infections and respiratory disorders. They are trained to consider the entire patient, taking into account their medical history, lifestyle, and social factors, which allows for a more personalized and effective approach to healthcare.

A key aspect of internal medicine is its emphasis on diagnostic acumen. Internists are often referred to as "diagnosticians" due to their ability to piece together clinical clues to arrive at accurate diagnoses. This skill is honed through rigorous training, which includes medical school, residency, and often further specialization through fellowships. The ability to diagnose complex and often interrelated conditions is what sets internists apart and makes them invaluable in the medical field.

Internal medicine is also distinguished by its commitment to evidence-based practice. Internists are trained to critically appraise medical literature, apply the latest research findings to patient care, and continuously update their knowledge to keep pace with advancements in medical science. This commitment to lifelong learning ensures that patients receive care that is grounded in the best available evidence, improving outcomes and fostering trust in the patient-physician relationship.

Another vital component of internal medicine is its role in preventive care. Internists are not only concerned with treating diseases but also with preventing them. They provide routine screenings, vaccinations, and counseling on lifestyle modifications to mitigate the risk of developing serious health conditions. This proactive approach helps to detect potential issues early and address them before they become more severe, ultimately enhancing the quality of life for patients.

Internal medicine encompasses various subspecialties, allowing internists to develop expertise in specific areas while maintaining a broad understanding of general health. Subspecialties such as cardiology, gastroenterology, endocrinology, and infectious diseases enable internists to provide highly specialized care while retaining the holistic perspective that is central to their practice. This versatility allows for comprehensive management of patients with complex, multisystem diseases.

The role of internists has become even more critical in the context of an aging population and the increasing prevalence of chronic diseases. As patients live longer and with more comorbidities, the need for skilled internists who can manage multiple health issues simultaneously is paramount. Their ability to coordinate care, work collaboratively with other specialists, and provide continuous support makes them essential in delivering effective and efficient healthcare.'''

    book6 = '''Good programming practices are essential for developing efficient, maintainable, and robust software. These practices not only improve the quality of the code but also facilitate collaboration among developers and ensure that software can be easily updated and scaled over time. Whether a programmer is working on a small personal project or a large, complex system, adhering to these best practices is crucial for success.

Code Readability:
One of the most fundamental aspects of good programming practices is writing readable code. Code readability refers to how easily other developers (or the original author at a later time) can understand and follow the code. This can be achieved through clear and consistent naming conventions, proper indentation, and thorough documentation. Descriptive variable and function names, along with meaningful comments, make the code self-explanatory and reduce the learning curve for new developers joining the project.

Modularization and Reusability:
Breaking down a program into smaller, manageable modules or functions is another cornerstone of good programming practice. This approach, known as modularization, not only makes the code easier to understand but also promotes reusability. Functions and modules should be designed to perform a single task or a closely related set of tasks. This separation of concerns allows developers to reuse code across different parts of the application or in future projects, reducing redundancy and the likelihood of bugs.

DRY Principle:
The DRY (Don't Repeat Yourself) principle is closely related to modularization and reusability. It emphasizes the importance of avoiding duplicate code by abstracting common functionality into reusable functions or modules. By adhering to the DRY principle, developers can ensure that changes or bug fixes need to be made in only one place, reducing the risk of inconsistencies and errors in the codebase.

Consistent Coding Style:
Maintaining a consistent coding style across a project is crucial for collaboration and code maintainability. Many teams adopt coding standards or style guides to ensure uniformity. These guidelines cover aspects such as naming conventions, code formatting, and comment styles. Tools like linters can automate the enforcement of coding standards, helping developers catch and correct deviations early in the development process.

Version Control:
Using version control systems, such as Git, is a best practice that cannot be overlooked. Version control allows developers to track changes to the codebase, collaborate with others, and revert to previous versions if necessary. It also facilitates code reviews, where peers can review changes before they are integrated into the main codebase, ensuring higher code quality and fostering knowledge sharing within the team.

Testing:
Writing tests is an integral part of good programming practices. Tests help ensure that the code works as expected and can prevent regressions when new features are added or existing ones are modified. Unit tests, which test individual components or functions, and integration tests, which test how different parts of the application work together, are both important. Test-driven development (TDD) is a practice where tests are written before the code itself, guiding the development process and ensuring that the code meets the requirements from the outset.

Error Handling and Logging:
Effective error handling and logging are critical for building robust applications. Errors should be anticipated and handled gracefully to prevent crashes and ensure a smooth user experience. Logging, on the other hand, provides valuable insights into the application's behavior, helping developers diagnose issues and understand the flow of execution. Both practices are essential for maintaining and troubleshooting applications, especially in production environments.

Security Considerations:
Security should be a primary concern throughout the development process. This includes validating and sanitizing user inputs to prevent injection attacks, using encryption to protect sensitive data, and following best practices for authentication and authorization. Regularly updating dependencies and libraries to patch known vulnerabilities is also crucial. By prioritizing security from the start, developers can protect their applications and users from potential threats.

Documentation:
Comprehensive documentation is vital for any software project. It includes comments within the code, as well as external documentation that describes the overall architecture, key components, and how to set up and use the software. Good documentation makes it easier for new developers to onboard, helps users understand and utilize the application effectively, and serves as a reference for future development and maintenance.

Continuous Improvement:
Finally, good programming practices involve a commitment to continuous improvement. This means regularly refactoring code to improve its structure and performance, staying updated with the latest tools and technologies, and being open to feedback and new ideas. By fostering a culture of continuous learning and improvement, developers can ensure that their skills and codebase evolve to meet changing demands and challenges.'''

    book7='''Relativity, a cornerstone of modern physics, fundamentally altered our understanding of space, time, and gravity. Formulated by Albert Einstein in the early 20th century, the theory of relativity comprises two interrelated theories: special relativity and general relativity. Both theories have profoundly impacted the field of physics and our comprehension of the universe.

Special relativity, introduced by Einstein in 1905, revolutionized the way we perceive space and time. Prior to this, classical mechanics, based on Isaac Newton's laws, held that space and time were absolute and unchanging. However, Einstein’s special relativity challenged these notions by proposing that the laws of physics are the same for all observers in uniform motion relative to one another. One of the key postulates of special relativity is that the speed of light in a vacuum is constant for all observers, regardless of their relative motion. This leads to the groundbreaking conclusion that space and time are intertwined into a single continuum known as spacetime. Special relativity also introduced the concept of time dilation, where time appears to slow down for objects moving at speeds close to the speed of light, and length contraction, where objects appear shorter in the direction of their motion. These ideas have been experimentally validated and have profound implications for our understanding of the universe.

General relativity, published by Einstein in 1915, extends the principles of special relativity to include acceleration and gravity. While special relativity deals with inertial frames of reference, general relativity addresses non-inertial frames and provides a new perspective on gravity. According to general relativity, gravity is not a force in the traditional sense but rather the result of the curvature of spacetime caused by the presence of mass and energy. Massive objects, such as stars and planets, warp the fabric of spacetime around them, and this curvature dictates the motion of objects. For instance, the orbits of planets around the sun and the paths of light rays passing near massive objects can be accurately described using general relativity. The theory has been confirmed through various experiments and observations, including the famous 1919 solar eclipse observation that demonstrated the bending of starlight around the sun.

The implications of relativity extend beyond theoretical physics and have practical applications in modern technology. For example, the Global Positioning System (GPS) relies on precise time measurements from satellites orbiting Earth. Because these satellites are moving at high speeds relative to Earth’s surface and are in a different gravitational field, both special and general relativity must be accounted for to ensure accurate positioning data. The theory of relativity also plays a crucial role in understanding phenomena such as black holes, neutron stars, and the expansion of the universe.

Despite its profound impact, relativity can be challenging to grasp, as it defies our intuitive understanding of space and time. It requires a shift from the Newtonian worldview of absolute space and time to a relativistic perspective where spacetime is dynamic and interconnected. Nonetheless, relativity has been validated through countless experiments and observations and remains a fundamental component of modern physics. It has not only deepened our understanding of the cosmos but also provided a framework for exploring new frontiers in science.

Einstein's theory of relativity represents one of the most significant achievements in the history of physics. Special relativity redefined our conception of space and time, while general relativity transformed our understanding of gravity and the structure of the universe. The principles of relativity have far-reaching implications, influencing both theoretical research and practical technologies. As we continue to explore the mysteries of the universe, relativity remains a vital and inspiring aspect of scientific inquiry, shaping our comprehension of the fundamental nature of reality.'''

    book8 = '''Kobe Bryant, who earned the nickname "Black Mamba" during his illustrious career, cultivated this mentality through an intense focus on personal growth and performance. For Bryant, Mamba Mentality was not just about being the best on the court but about embracing challenges, persevering through adversity, and constantly striving to improve. His approach to the game was marked by a relentless pursuit of perfection, where every practice session, game, and moment of preparation was an opportunity to refine his skills and elevate his performance. This mindset, characterized by an unwavering dedication to excellence, inspired countless individuals both within and beyond the realm of basketball.

The essence of Mamba Mentality lies in its emphasis on hard work and resilience. Kobe Bryant's journey was one of continuous effort and dedication, underscoring the importance of putting in the necessary hours to achieve one's goals. His famous "5 a.m. workouts" and rigorous training routines were a testament to his belief in the value of discipline and perseverance. Mamba Mentality teaches that success is not merely a product of talent but a result of relentless effort and an unyielding commitment to overcoming obstacles. It challenges individuals to confront their limitations, embrace the discomfort of growth, and transform setbacks into opportunities for advancement.

Beyond its application in sports, Mamba Mentality serves as a powerful framework for personal and professional development. It encourages individuals to adopt a growth mindset, where challenges are viewed as chances for improvement rather than insurmountable barriers. This philosophy fosters a sense of accountability and self-belief, motivating people to take ownership of their goals and pursue them with passion and determination. Whether in business, academics, or personal relationships, Mamba Mentality promotes a proactive approach to achieving excellence and navigating the complexities of life.

Moreover, Mamba Mentality emphasizes the importance of leaving a lasting legacy through one's actions and contributions. Kobe Bryant's influence extended far beyond the basketball court, as he sought to inspire and mentor others, sharing his experiences and insights with the next generation. His legacy embodies the idea that true greatness is measured not only by individual achievements but also by the positive impact one has on others. Mamba Mentality encourages individuals to consider how their efforts and attitudes can inspire and uplift those around them, creating a ripple effect of motivation and excellence.

Mamba Mentality represents a powerful and transformative philosophy rooted in Kobe Bryant's relentless pursuit of excellence and personal growth. It encompasses the principles of hard work, resilience, and a commitment to overcoming challenges, serving as a guide for achieving success and making a meaningful impact. By embracing Mamba Mentality, individuals can cultivate a mindset that drives them to excel in their endeavors, inspire others, and leave a lasting legacy of excellence.'''

    book9 = '''Vedic Mathematics, a system of mathematical techniques and shortcuts derived from ancient Indian texts, offers a unique and efficient approach to arithmetic and algebra. Rooted in the Vedas, the sacred scriptures of Hinduism, Vedic Mathematics was rediscovered and popularized in the early 20th century by Bharati Krishna Tirthaji, a Hindu scholar and mathematician. This system is characterized by its simplicity, versatility, and the ability to perform complex calculations with ease.

The origins of Vedic Mathematics can be traced back to the Vedic period, which dates approximately between 1500 and 500 BCE. The Vedas, particularly the "Sutras" (aphorisms) within them, are the foundational texts from which Vedic Mathematics draws its principles. These Sutras offer concise and profound mathematical formulas and techniques that cover a broad range of topics, including arithmetic, algebra, geometry, and calculus. The discovery of these techniques in the modern era brought to light an ancient mathematical tradition that had been largely forgotten.

One of the most striking features of Vedic Mathematics is its emphasis on mental calculation and speed. The system employs a variety of techniques, known as "sutras" or "formulae," which simplify and expedite the process of solving mathematical problems. For instance, the "Vertically and Crosswise" method, used for multiplication, allows for rapid calculations by breaking down numbers into smaller, more manageable parts. Similarly, the "Nikhilam" method simplifies division and subtraction, making these operations more intuitive and less error-prone.

Vedic Mathematics also introduces innovative techniques for squaring numbers, finding square roots, and solving algebraic equations. These methods are designed to reduce the complexity of calculations and provide alternative approaches to traditional arithmetic operations. For example, the "Urdhva Tiryak" Sutra (Vertical and Crosswise) offers a systematic way to multiply large numbers, while the "Anurupye" Sutra (Proportionality) helps in solving algebraic problems involving ratios and proportions. These techniques highlight the versatility of Vedic Mathematics and its potential to enhance computational efficiency.

In addition to its practical applications, Vedic Mathematics fosters a deeper understanding of mathematical concepts. By exploring the underlying principles and patterns within the system, students and practitioners can develop a more intuitive grasp of mathematical operations. This holistic approach encourages a broader appreciation of mathematics as a dynamic and interconnected discipline, rather than a collection of isolated techniques.

The resurgence of interest in Vedic Mathematics in recent decades has led to its incorporation into educational curricula and training programs. Many educators and institutions recognize the value of Vedic techniques in enhancing mathematical skills and promoting mental agility. By integrating these methods into modern teaching practices, educators aim to make mathematics more accessible and engaging for students of all ages.

Despite its many advantages, Vedic Mathematics is not without its challenges. Critics argue that the system's techniques, while efficient, may not always align with conventional mathematical methods or standards. Additionally, the limited scope of some techniques may restrict their applicability in more advanced or specialized areas of mathematics. Nonetheless, the enduring appeal of Vedic Mathematics lies in its ability to offer alternative solutions and perspectives, complementing rather than replacing traditional approaches.'''
    
    book10 = '''Magnetism, a fundamental force of nature, plays a crucial role in both the macroscopic world and the microscopic realm of particles. From the compasses that guide explorers to the electromagnetic fields that drive modern technology, magnetism is a pervasive and essential aspect of our daily lives. Rooted in ancient observations and refined through centuries of scientific inquiry, magnetism provides a window into the forces that govern the behavior of matter.

The phenomenon of magnetism was first observed in ancient civilizations, with the earliest recorded use of magnets dating back to around 600 BCE in ancient Greece. The term "magnet" itself is derived from Magnesia, a region in Asia Minor known for its naturally occurring lodestones, which are magnetic rocks composed of magnetite. These early observations laid the groundwork for understanding the properties of magnets, which attract and repel certain materials, such as iron.

The modern scientific understanding of magnetism began to take shape in the 19th century with the work of pioneers such as Hans Christian Oersted, André-Marie Ampère, and Michael Faraday. Oersted's discovery in 1820 that an electric current generates a magnetic field around it was a breakthrough that linked electricity and magnetism. This revelation led to the development of electromagnetism, a branch of physics that explores the interactions between electric currents and magnetic fields.

Faraday's experiments further advanced the field by demonstrating electromagnetic induction—the principle that a changing magnetic field can induce an electric current in a conductor. This principle is the foundation of many technological applications, including electric generators and transformers. Faraday’s work established the concept of the electromagnetic field, a theoretical construct that describes how electric and magnetic forces interact and propagate through space.

Magnetism at the atomic and molecular level is governed by the behavior of electrons and their intrinsic magnetic moments. Electrons have a property known as "spin," which contributes to the magnetic properties of materials. In certain materials, such as ferromagnets like iron, the magnetic moments of electrons align in a uniform direction, resulting in a net magnetic field. This alignment can be influenced by external magnetic fields, leading to phenomena such as magnetic saturation and hysteresis.

The study of magnetism also encompasses the concept of magnetic domains, which are regions within a material where the magnetic moments of atoms are aligned in the same direction. When a material is magnetized, the magnetic domains align to create a macroscopic magnetic field. Understanding the behavior of magnetic domains has practical implications for the design of magnetic materials and devices, such as hard drives and magnetic sensors.

In addition to its fundamental scientific significance, magnetism has wide-ranging technological applications. Magnetic materials are integral to many modern devices, including electric motors, transformers, and magnetic resonance imaging (MRI) machines. MRI technology, which relies on strong magnetic fields and radio waves, allows for detailed imaging of the human body's internal structures, revolutionizing medical diagnostics.

Magnetism also plays a vital role in geophysics and space exploration. The Earth's magnetic field, generated by the movement of molten iron in its core, protects the planet from harmful solar radiation and plays a crucial role in navigation. Studying planetary magnetism and magnetic fields in space helps scientists understand the conditions on other planets and celestial bodies, contributing to our knowledge of the solar system and beyond.

Despite its importance, many aspects of magnetism remain subjects of active research. The study of superconductors, materials that exhibit zero electrical resistance and perfect magnetic shielding at very low temperatures, continues to reveal new insights into the behavior of magnetic fields. Additionally, research into magnetic materials for data storage, spintronics, and quantum computing holds the promise of advancing technology and expanding our understanding of fundamental physics.'''
    
    
    book11 = '''Insulin resistance, a condition in which the body’s cells become less responsive to the hormone insulin, has emerged as a significant health concern in the modern world. This metabolic disorder is closely linked to several chronic diseases, including type 2 diabetes, cardiovascular disease, and obesity. Understanding insulin resistance involves examining its underlying mechanisms, risk factors, and impact on health, as well as exploring strategies for prevention and management.

Insulin is a hormone produced by the pancreas that plays a crucial role in regulating blood glucose levels. When we eat, insulin facilitates the uptake of glucose into cells, where it is used for energy or stored for later use. In individuals with insulin resistance, however, the cells’ ability to respond to insulin is impaired. As a result, glucose accumulates in the bloodstream, leading to elevated blood sugar levels. To compensate, the pancreas produces more insulin, leading to hyperinsulinemia. Over time, this increased demand can exhaust the pancreas, potentially resulting in type 2 diabetes.

The mechanisms underlying insulin resistance are complex and involve multiple factors. At the cellular level, insulin resistance occurs when the insulin receptor pathways become disrupted. This can be due to changes in the insulin receptor itself, alterations in downstream signaling molecules, or increased levels of inflammatory cytokines. Additionally, excessive accumulation of fatty acids in muscle and liver cells can interfere with insulin signaling, contributing to resistance. This cellular dysfunction is often exacerbated by systemic factors such as chronic inflammation, oxidative stress, and hormonal imbalances.

Several risk factors are associated with the development of insulin resistance. Lifestyle factors, such as a sedentary lifestyle and poor dietary choices, play a significant role. Diets high in refined carbohydrates, sugars, and unhealthy fats can contribute to obesity, which is a major risk factor for insulin resistance. Obesity, particularly abdominal or visceral fat, is linked to increased levels of inflammatory markers and insulin resistance. Genetic predisposition also plays a role, with some individuals being more susceptible to insulin resistance due to inherited traits.

The impact of insulin resistance on health extends beyond elevated blood sugar levels. It is closely associated with a cluster of conditions known as metabolic syndrome, which includes high blood pressure, elevated cholesterol levels, and increased abdominal fat. Metabolic syndrome significantly raises the risk of cardiovascular disease, stroke, and type 2 diabetes. Additionally, insulin resistance can lead to other complications such as polycystic ovary syndrome (PCOS) and non-alcoholic fatty liver disease (NAFLD).

Addressing insulin resistance requires a multifaceted approach that focuses on lifestyle modifications and medical management. Regular physical activity is one of the most effective ways to improve insulin sensitivity. Exercise helps increase glucose uptake by muscle cells and reduces body fat, both of which contribute to better insulin function. Dietary changes are also crucial; consuming a balanced diet rich in whole grains, fruits, vegetables, lean proteins, and healthy fats can help regulate blood sugar levels and reduce inflammation.

Weight management is another key component in managing insulin resistance. For individuals who are overweight or obese, even modest weight loss can improve insulin sensitivity and reduce the risk of developing type 2 diabetes. Behavioral strategies, such as mindful eating and stress management, can further support weight loss and overall metabolic health.

In some cases, medical interventions may be necessary to manage insulin resistance. Medications such as metformin, which improves insulin sensitivity, may be prescribed to individuals at risk of or diagnosed with type 2 diabetes. Additionally, managing associated conditions such as high blood pressure and high cholesterol through medication and lifestyle changes is important for reducing the overall risk of cardiovascular disease.'''
    
    
    ebooks = [EBook(book_name = "The History of Ancient World", section_id = 1, author = "Susan Wise Bauer",created_by = "librarian@123", content=book1),
                EBook(book_name = "Guns, Germs, and Steel", section_id = 1, author = "Jared Diamond", created_by = "librarian@123", content=book2),
                EBook(book_name = "Agile Software Craftsmanship", section_id = 3, author = "Robert C. Martin", created_by = "librarian@123", content=book3),
                EBook(book_name = "A Biography of Cancer", section_id = 2, author = "Siddhartha Mukherjee", created_by = "librarian@123", content=book4),
                EBook(book_name = "Principles of Internal Medicine", section_id = 2, author = "Harrison's", created_by = "librarian@123", content=book5),
                EBook(book_name = "The Pragmatic Programmer", section_id = 3, author = "Andrew Hunt, David Thomas", created_by = "librarian@123", content=book6),
                EBook(book_name = "Special Relativity", section_id = 4, author = "Valerio Faroni", created_by = "librarian@123", content=book7),
                EBook(book_name = "The Mamba Mentality", section_id = 5, author = "Kobe Bryant", created_by = "librarian@123", content=book8),
                EBook(book_name = "Vedic Maths", section_id = 6, author = "Vidhya Vikram", created_by = "librarian@123", content=book9),
                EBook(book_name = "Magnetism", section_id = 4, author = "Stephen J. Blundell", created_by = "librarian@123", content=book10),
                EBook(book_name = "Insulin Resistance Guide", section_id = 2, author = "Alex Johnson", created_by = "librarian@123", content=book11),
                ]
    for book in ebooks:
        if not EBook.query.filter_by(book_name = book.book_name).first():
            db.session.add(book)
            db.session.commit()
            
            
    # datetime(2024, 7, 31, 15, 30, 0)
    issues = [IssueReturn(user_id=2, ebook_id=1, issue_date=datetime(2024, 7, 5, 15, 30, 0), return_date=datetime(2024, 7, 12, 15, 30, 0), returned_on=datetime(2024, 7, 10, 10, 31, 2), status='returned', created_by='user1@123', date_created=datetime(2024, 7, 5, 15, 30, 0), updated_by='user1@123', updated_date=datetime(2024, 7, 10, 10, 31, 2)),
              IssueReturn(user_id=3, ebook_id=2, issue_date=datetime(2024, 7, 27, 16, 45, 0), return_date=datetime(2024, 8, 3, 16, 45, 0), returned_on=datetime(2024, 8, 3, 16, 45, 0), status='returned', created_by='user2@123', date_created=datetime(2024, 7, 26, 16, 45, 0), updated_by='lms', updated_date=datetime(2024, 7, 26, 16, 45, 0)),
              IssueReturn(user_id=4, ebook_id=1, issue_date=datetime(2024, 7, 28, 10, 30, 0), return_date=datetime(2024, 8, 4, 10, 30, 0), returned_on=datetime(2024, 8, 4, 10, 30, 0), status='returned', created_by='user3@123', date_created=datetime(2024, 7, 28, 10, 30, 0), updated_by='lms', updated_date=datetime(2024, 7, 28, 10, 30, 0)),
              IssueReturn(user_id=5, ebook_id=3, issue_date=datetime(2024, 7, 23, 21, 30, 0), return_date=datetime(2024, 7, 30, 21, 30, 0), returned_on=datetime(2024, 7, 23, 21, 30, 0), status='returned', created_by='user4@123', date_created=datetime(2024, 7, 23, 21, 30, 0), updated_by='user4@123', updated_date=datetime(2024, 7, 30, 10, 31, 2)),
              IssueReturn(user_id=3, ebook_id=6, issue_date=datetime(2024, 7, 26, 8, 30, 0), return_date=datetime(2024, 8, 2, 8, 30, 0), returned_on=datetime(2024, 7, 29, 10, 31, 2), status='returned', created_by='user2@123', date_created=datetime(2024, 7, 26, 8, 30, 0), updated_by='user2@123', updated_date=datetime(2024, 7, 29, 10, 31, 2)),
              IssueReturn(user_id=2, ebook_id=6, issue_date=datetime(2024, 7, 27, 15, 30, 0), return_date=datetime(2024, 8, 3, 15, 30, 0), returned_on=datetime(2024, 8, 1, 15, 30, 0), status='returned', created_by='user1@123', date_created=datetime(2024, 7, 27, 15, 30, 0), updated_by='user1@123', updated_date=datetime(2024, 7, 27, 20, 30, 0)),
              IssueReturn(user_id=4, ebook_id=5, issue_date=datetime(2024, 7, 29, 15, 30, 0), return_date=datetime(2024, 8, 5, 15, 30, 0), returned_on=datetime(2024, 8, 5, 15, 30, 0), status='returned', created_by='user3@123', date_created=datetime(2024, 7, 29, 15, 30, 0), updated_by='lms', updated_date=datetime(2024, 7, 29, 15, 30, 0)),
              IssueReturn(user_id=5, ebook_id=6, issue_date=datetime(2024, 7, 28, 15, 30, 0), return_date=datetime(2024, 8, 4, 15, 30, 0), returned_on=datetime(2024, 8, 4, 15, 30, 0), status='returned', created_by='user4@123', date_created=datetime(2024, 7, 28, 15, 30, 0), updated_by='lms', updated_date=datetime(2024, 7, 28, 15, 30, 0)),
              IssueReturn(user_id=2, ebook_id=7, issue_date=None, return_date=None, returned_on=None, status='requested', created_by='user1@123', date_created=datetime(2024, 8, 1, 11, 4, 17), updated_by=None, updated_date=datetime(2024, 8, 1, 11, 4, 17)),
              IssueReturn(user_id=4, ebook_id=9, issue_date=None, return_date=None, returned_on=None, status='requested', created_by='user3@123', date_created=datetime(2024, 8, 2, 13, 14, 12), updated_by=None, updated_date=datetime(2024, 8, 2, 13, 14, 12)),
              IssueReturn(user_id=5, ebook_id=10, issue_date=None, return_date=None, returned_on=None, status='requested', created_by='user3@123', date_created=datetime(2024, 8, 3, 17, 11, 42), updated_by=None, updated_date=datetime(2024, 8, 3, 17, 11, 42)),
              IssueReturn(user_id=3, ebook_id=8, issue_date=datetime(2024, 8, 3, 15, 30, 0), return_date=datetime(2024, 8, 10, 15, 30, 0), returned_on=None, status='issued', created_by='user4@123', date_created=datetime(2024, 8, 3, 15, 30, 0), updated_by='librarian@123', updated_date=datetime(2024, 8, 3, 17, 30, 0)),
              IssueReturn(user_id=4, ebook_id=2, issue_date=datetime(2024, 8, 3, 10, 40, 0), return_date=datetime(2024, 8, 10, 10, 40, 0), returned_on=None, status='issued', created_by='user5@123', date_created=datetime(2024, 8, 3, 15, 30, 0), updated_by='librarian@123', updated_date=datetime(2024, 8, 3, 15, 30, 0)),
              IssueReturn(user_id=2, ebook_id=1, issue_date=datetime(2024, 8, 4, 15, 30, 0), return_date=datetime(2024, 8, 10, 15, 30, 0), returned_on=None, status='issued', created_by='user3@123', date_created=datetime(2024, 8, 4, 15, 30, 0), updated_by='librarian@123', updated_date=datetime(2024, 8, 4, 20, 30, 0)),
              IssueReturn(user_id=5, ebook_id=4, issue_date=datetime(2024, 8, 5, 8, 27, 32), return_date=datetime(2024, 8, 12, 8, 27, 32), returned_on=None, status='issued', created_by='user6@123', date_created=datetime(2024, 8, 5, 8, 27, 42), updated_by='librarian@123', updated_date=datetime(2024, 8, 5, 19, 55, 0)),
              ]
    for issue in issues:
        db.session.add(issue)
        db.session.commit()
    
    ratings = [Ratings(user_id = 2, ebook_id = 1, rating = 3, created_by='user1@123'),
               Ratings(user_id = 3, ebook_id = 2, rating = 5, created_by='user2@123'),
               Ratings(user_id = 4, ebook_id = 1, rating = 2, created_by='user3@123'),
               Ratings(user_id = 5, ebook_id = 3, rating = 1, created_by='user4@123'),
               Ratings(user_id = 3, ebook_id = 6, rating = 4, created_by='user2@123'),
               Ratings(user_id = 2, ebook_id = 6, rating = 5, created_by='user1@123'),
               Ratings(user_id = 4, ebook_id = 5, rating = 1, created_by='user3@123'),
               Ratings(user_id = 5, ebook_id = 6, rating = 3, created_by='user4@123')]
    for rate in ratings:
        db.session.add(rate)
        db.session.commit()