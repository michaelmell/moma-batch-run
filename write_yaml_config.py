import yaml

tracking_config_1 = {
                    'path': '/media/micha/T7/data_michael_mell/moma_test_data/000_development/feature/20220121-fix-loading-of-curated-datasets/Lis/20211026/20211026__lis__process_positions__output__20211101-013152',
                    'position': {
                        0: {
                            'tmax': 100,
                            'gl': [12,23]
                            },
                        15: {
                            'tmax': 100,
                            'gl': []
                            },
                        21: {},
                        },
                    }

with open('tracking_config_1.yaml', 'w') as f:
    data = yaml.dump(tracking_config_1, f, sort_keys=True, default_flow_style=False)


#######################


tracking_config_2 = {
                    'path': '/media/micha/T7/data_michael_mell/moma_test_data/000_development/feature/20220121-fix-loading-of-curated-datasets/Lis/20211026/20211026__lis__process_positions__output__20211101-013152',
                    'position': {},
                    }

with open('tracking_config_2.yaml', 'w') as f:
    data = yaml.dump(tracking_config_2, f, sort_keys=True, default_flow_style=False)


#######################


tracking_config_3 = {
                    'path': '/media/micha/T7/data_michael_mell/moma_test_data/000_development/feature/20220121-fix-loading-of-curated-datasets/Lis/20211026/20211026__lis__process_positions__output__20211101-013152',
                    'position': {},
                    }

with open('tracking_config_3.yaml', 'w') as f:
    data = yaml.dump(tracking_config_3, f, sort_keys=True, default_flow_style=False)


#######################

