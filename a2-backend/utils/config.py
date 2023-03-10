class Config:
    # list of memcache servers
    memcache_ip = [
        ('localhost', 5010),
        ('localhost', 5011),
        ('localhost', 5012),
        ('localhost', 5013),
        ('localhost', 5014),
        ('localhost', 5015),
        ('localhost', 5016),
        ('localhost', 5017),
    ]
    scaler_ip = ('localhost', 5002)
    rds_ip = "biggerdb.cvtl8zx5dggi.us-east-1.rds.amazonaws.com"
    rds_user = "root"
    rds_password = "ece1779pass"