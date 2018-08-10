"""
Sample definition validation errors
Used to test printing out reports.
"""
errors = {
    'content': {
        'direct': ['Content types collection must be a list'],
        'collection': {

            # content type
            0: {
                'name': ['Content type must have a name'],
                'handle': ['Content type must have a handle'],
                'description': ['Content type must have a description'],
                'fields': {
                    'direct': ['Content type must have fields'],
                    'collection': {
                        0: {
                            'name': ['Field requires a name'],
                            'handle': ['Field requires a handle'],
                            'type': ['Field requires a type'],
                            'filters': {
                                'direct': ['Collection must be a list'],
                                'collection': {
                                    0: {
                                        'type': [
                                            'Requires type',
                                            'Not importable'
                                        ],
                                    },
                                    1: {
                                        'type': [
                                            'Requires type',
                                            'Not importable'
                                        ],
                                    },
                                }
                            },
                            'validators': {
                                'direct': ['Collection must be a list'],
                                'collection': {
                                    0: {
                                        'type': [
                                            'Requires type',
                                            'Not importable'
                                        ],
                                    },
                                    1: {
                                        'type': [
                                            'Requires type',
                                            'Not importable'
                                        ],
                                    },
                                }

                            }
                        },
                        1: {
                            'name': ['Name not unique'],
                            'handle': ['Handle not unique'],
                            'type': ['Type does not exist'],
                            'filters': {
                                'direct': ['Collection must be a list'],
                                'collection': {
                                    0: {
                                        'type': [
                                            'Requires type',
                                            'Not importable'
                                        ],
                                    },
                                    1: {
                                        'type': [
                                            'Requires type',
                                            'Not importable'
                                        ],
                                    },
                                }
                            },
                            'validators': {
                                'direct': ['Collection must be a list'],
                                'collection': {
                                    0: {
                                        'type': [
                                            'Requires type',
                                            'Not importable'
                                        ],
                                    },
                                    1: {
                                        'type': [
                                            'Requires type',
                                            'Not importable'
                                        ],
                                    },
                                }

                            }
                        },
                    }
                }
            },

            # content type
            1: {
                'name': ['Content type must have a name'],
                'handle': ['Content type must have a handle'],
                'description': ['Content type must have a description'],
                'fields': {
                    'direct': ['Content type must have fields'],
                    'collection': {
                        0: {
                            'name': ['Field requires a name'],
                            'handle': ['Field requires a handle'],
                            'type': ['Field requires a type'],
                            'filters': {
                                'direct': ['Collection must be a list'],
                                'collection': {
                                    0: {
                                        'type': [
                                            'Requires type',
                                            'Not importable'
                                        ],
                                    },
                                    1: {
                                        'type': [
                                            'Requires type',
                                            'Not importable'
                                        ],
                                    },
                                }
                            },
                            'validators': {
                                'direct': ['Collection must be a list'],
                                'collection': {
                                    0: {
                                        'type': [
                                            'Requires type',
                                            'Not importable'
                                        ],
                                    },
                                    1: {
                                        'type': [
                                            'Requires type',
                                            'Not importable'
                                        ],
                                    },
                                }

                            }
                        },
                        1: {
                            'name': ['Name not unique'],
                            'handle': ['Handle not unique'],
                            'type': ['Type does not exist'],
                            'filters': {
                                'direct': ['Collection must be a list'],
                                'collection': {
                                    0: {
                                        'type': [
                                            'Requires type',
                                            'Not importable'
                                        ],
                                    },
                                    1: {
                                        'type': [
                                            'Requires type',
                                            'Not importable'
                                        ],
                                    },
                                }
                            },
                            'validators': {
                                'direct': ['Collection must be a list'],
                                'collection': {
                                    0: {
                                        'type': [
                                            'Requires type',
                                            'Not importable'
                                        ],
                                    },
                                    1: {
                                        'type': [
                                            'Requires type',
                                            'Not importable'
                                        ],
                                    },
                                }

                            }
                        },
                    }
                }
            },

        }
    }
}