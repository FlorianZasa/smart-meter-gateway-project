db.createUser({
    user: 'sa',
    pwd: 'password',
    roles: [
      { role: 'readWrite', db: 'smg' },
      { role: 'dbAdmin', db: 'smg' }
    ]
  });
  