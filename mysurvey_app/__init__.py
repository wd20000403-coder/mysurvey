from otree.api import *

doc = """
Survey on fairness perceptions: luck vs. effort in online games
"""


class C(BaseConstants):
    NAME_IN_URL = 'mysurvey_app'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # consent
    consent = models.BooleanField(
        label='Ich stimme der freiwilligen Teilnahme an dieser Studie zu.'
    )

    # demographics
    age = models.StringField(
        label='1. Wie alt sind Sie?',
        choices=[
            'Unter 18',
            '18–24',
            '25–34',
            '35–44',
            '45 oder älter',
            'Keine Angabe',
        ],
        widget=widgets.RadioSelect,
    )

    gender = models.StringField(
        label='2. Welches Geschlecht haben Sie?',
        choices=[
            'weiblich',
            'männlich',
            'divers',
            'keine Angabe',
        ],
        widget=widgets.RadioSelect,
    )

    status = models.StringField(
        label='3. Welcher der folgenden Kategorien entspricht Ihrem aktuellen Status am ehesten?',
        choices=[
            'Studierende/r',
            'Erwerbstätig (Vollzeit oder Teilzeit)',
            'Selbstständig',
            'Nicht erwerbstätig (z. B. arbeitssuchend)',
        ],
        widget=widgets.RadioSelect,
    )

    education = models.StringField(
        label='4. Welcher ist der höchste Bildungsabschluss, den Sie erworben haben?',
        choices=[
            'Keinen Abschluss',
            'Hauptschulabschluss',
            'Mittlere Hochschulreife',
            'Fachhochschulreife / Abitur',
            'Anderer Schulabschluss',
            'Bachelor',
            'Master',
            'Duale Berufsausbildung',
            'Meistergrad',
            'Promotion (Dr.)',
            'Anderer beruflicher Abschluss',
        ],
        widget=widgets.RadioSelect,
    )

    income = models.StringField(
        label='5. Wie hoch ist Ihr monatlich verfügbares Einkommen bzw. Budget ungefähr?',
        choices=[
            'Unter 800 €',
            '800–1.500 €',
            '1.500–2.500 €',
            'Über 2.500 €',
            'Keine Angabe',
        ],
        widget=widgets.RadioSelect,
    )

    gaming_frequency = models.StringField(
        label='6. Wie häufig spielen Sie Videospiele?',
        choices=[
            'häufig',
            'gelegentlich',
            'fast nie',
        ],
        widget=widgets.RadioSelect,
    )

    # scenario assignment
    scenario_type = models.StringField()

    # manipulation check
    mechanism_main = models.StringField(
        label='7.1 Wodurch entstehen in diesem Szenario hauptsächlich die Leistungsunterschiede zwischen den Spielern?',
        choices=[
            'Zufall / Glück',
            'Anstrengung der Spieler',
            'Weiß nicht',
        ],
        widget=widgets.RadioSelect,
    )

    # fairness items (1-5)
    fairness_1 = models.IntegerField(
        label='F1. Ich halte diese Art von Leistungsunterschieden für fair.',
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal,
    )
    fairness_2 = models.IntegerField(
        label='F2. Die Vorteile stärkerer Spieler sind aus meiner Sicht „verdient“.',
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal,
    )
    fairness_3 = models.IntegerField(
        label='F3. Dieses Spielsystem ist gegenüber durchschnittlichen Spielern unfair.',
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal,
    )

    # support items (1-5)
    support_1 = models.IntegerField(
        label='F1. Unterstützen Sie die durch dieses Spielsystem entstehenden Leistungsunterschiede?',
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal,
    )
    support_2 = models.IntegerField(
        label='F2. Unterstützen Sie, dass stärkere Spieler aufgrund dieses Spielsystems Vorteile haben?',
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal,
    )
    support_3 = models.IntegerField(
        label='F3. Unterstützen Sie dieses Spielsystem, obwohl es durchschnittliche Spieler benachteiligt?',
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal,
    )

    rebalance = models.StringField(
        label='7.4 Wenn nur eine Maßnahme gewählt werden könnte, welche würden Sie am ehesten unterstützen?',
        choices=[
            'Keine Rebalancing-Mechanismen',
            'Zusätzliche Unterstützung für schwächere Spieler',
            'Einschränkung der Vorteile stärkerer Spieler',
            'Kombination aus Unterstützung und Einschränkung',
        ],
        widget=widgets.RadioSelect,
    )


def creating_session(subsession: Subsession):
    players = subsession.get_players()
    for i, p in enumerate(players):
        if i % 2 == 0:
            p.scenario_type = 'luck'
        else:
            p.scenario_type = 'effort'


class Consent(Page):
    form_model = 'player'
    form_fields = ['consent']

    @staticmethod
    def error_message(player, values):
        if not values['consent']:
            return 'Sie müssen der Teilnahme zustimmen, um fortzufahren.'


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'status', 'education', 'income', 'gaming_frequency']


class Scenario(Page):
    form_model = 'player'
    form_fields = [
        'mechanism_main',
        'fairness_1',
        'fairness_2',
        'fairness_3',
        'support_1',
        'support_2',
        'support_3',
        'rebalance',
    ]

    @staticmethod
    def vars_for_template(player: Player):
        if player.scenario_type == 'luck':
            scenario_title = '7. Szenario'
            scenario_text = """
In einem Online-Spiel beginnen alle Spielerinnen und Spieler mit den gleichen Startbedingungen.
Die Unterschiede in der Spielstärke entstehen hauptsächlich durch einen zufallsbasierten Ziehmechanismus (z. B. „Gacha“):
Alle erhalten die gleiche Anzahl an Ziehversuchen, die Ergebnisse sind jedoch vollständig zufällig.
Einige Spieler ziehen sehr starke Charaktere, andere nicht.
Die Leistungsunterschiede zwischen den Spielern entstehen daher hauptsächlich durch Glück.
"""
        else:
            scenario_title = '7. Szenario'
            scenario_text = """
In einem Online-Spiel beginnen alle Spielerinnen und Spieler mit den gleichen Startbedingungen.
Die Unterschiede in der Spielstärke entstehen hauptsächlich durch individuelle Anstrengung und Investition:
Spieler können durch Zeitaufwand, das Erledigen von Aufgaben und das Üben ihrer Fähigkeiten stärker werden.
Wer mehr investiert, erzielt bessere Ergebnisse.
Die Leistungsunterschiede zwischen den Spielern entstehen daher hauptsächlich durch persönliche Anstrengung.
"""
        return dict(
            scenario_title=scenario_title,
            scenario_text=scenario_text,
        )


class ThankYou(Page):
    pass


page_sequence = [Consent, Demographics, Scenario, ThankYou]