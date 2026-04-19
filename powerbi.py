import os


current_dir = os.path.dirname(os.path.abspath(__file__))


def _get_img(name):
    return os.path.join(current_dir, 'images', name)


def show_powerbi_insights():
    metrics = {
        'avg_revenue': '85K PKR',
        'peak_domain': 'AI',
        'critical_sector': 'BA',
    }

    visualizations = {
        'field_distribution': _get_img('piechart.png'),
        'earning_potential': _get_img('bar.png'),
        'intelligence_matrix': _get_img('matrix.png'),
    }

    image_status = {
        name: {'path': path, 'exists': os.path.exists(path)}
        for name, path in visualizations.items()
    }

    smart_analysis = [
        'AI DOMAIN: EXTREME GROWTH DETECTED',
        'SOFTWARE ENG: HIGH STABILITY RATING',
        'MARKET ALERT: BA SECTOR SATURATION',
        'SKILL GAP: REVENUE LOSS IDENTIFIED',
    ]

    recommended_vectors = {
        'priority': ['AI Architect', 'Data Scientist', 'ML Engineer'],
        'strategic': ['Cloud Expert', 'Cyber Security', 'DevOps'],
        'upgrade': ['Business Tech', 'Digital Marketing', 'FinTech'],
    }

    return {
        'metrics': metrics,
        'visualizations': image_status,
        'smart_analysis': smart_analysis,
        'recommended_vectors': recommended_vectors,
    }