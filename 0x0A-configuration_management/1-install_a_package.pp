class flask_installation {
  # Ensure pip3 is present; adjust this accordingly if not already managed elsewhere in your Puppet code
  package { 'python3-pip':
    ensure => installed,
  }

  # Execute pip3 to install the specific version of Flask
  exec { 'install-flask':
    command     => 'pip3 install Flask==2.1.0',
    unless      => 'pip3 freeze | grep Flask==2.1.0',
    require     => Package['python3-pip'],
    path        => ['/bin', '/usr/bin'],
    environment => 'PATH=/usr/bin:/bin:/usr/local/bin', # Ensure pip3 is in the PATH
  }
}

include flask_installation
