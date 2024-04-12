# Puppet manifest to install Flask version 2.1.0

# Ensure pip3 is installed
package { 'python3-pip':
  ensure => installed,
}

# Ensure Flask is installed using pip3
exec { 'install-flask':
  command => '/usr/bin/pip3 install Flask==2.1.0',
  unless  => '/usr/bin/pip3 freeze | grep Flask==2.1.0',
  require => Package['python3-pip'],
}
