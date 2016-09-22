#!/bin/sh -xe

OS_VERSION=$1
CVMFS_EXTERNAL_URL=$2

# Clean the yum cache
yum -y clean all
yum -y clean expire-cache

# First, install all the needed packages.
rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-${OS_VERSION}.noarch.rpm

# Broken mirror?
echo "exclude=mirror.beyondhosting.net" >> /etc/yum/pluginconf.d/fastestmirror.conf

yum -y install yum-plugin-priorities
rpm -Uvh https://repo.grid.iu.edu/osg/3.3/osg-3.3-el${OS_VERSION}-release-latest.rpm

yum -y install osg-oasis

echo "user_allow_other" >> /etc/fuse.conf

echo "CVMFS_HTTP_PROXY=DIRECT" >> /etc/cvmfs/default.local
echo "CVMFS_EXTERNAL_URL=$CVMFS_EXTERNAL_URL" >> /etc/cvmfs/domain.d/osgstorage.org.local

mkdir -p /cvmfs/stash.osgstorage.org
mkdir -p /cvmfs/nova.osgstorage.org
mkdir -p /cvmfs/config-osg.opensciencegrid.org

mount -t cvmfs config-osg.opensciencegrid.org /cvmfs/config-osg.opensciencegrid.org
mount -t cvmfs stash.osgstorage.org /cvmfs/stash.osgstorage.org
mount -t cvmfs nova.osgstorage.org /cvmfs/nova.osgstorage.org

# Test Stash
result=`md5sum /cvmfs/stash.osgstorage.org/user/dweitzel/public/blast/queries/query1 | awk '{print $1;}'`

if [ "$result" != "12bdb9a96cd5e8ca469b727a81593201" ]; then
  journalctl --no-pager
  exit 1
fi

# Test Nova
result=`md5sum /cvmfs/nova.osgstorage.org/pnfs/fnal.gov/usr/nova/data/flux/gsimple/nova_gsimple_flux.ls | awk '{print $1;}'`

if [ "$result" != "8704291ceaf4f09924cdfb2dc4298f01" ]; then
  journalctl --no-pager
  exit 1
fi

# Check the update times of some special files
for repo in /cvmfs/nova.osgstorage.org/pnfs /cvmfs/stash.osgstorage.org/user/bbockelm; do
  if test ! `find $repo -maxdepth 0 -mtime -1`; then
    echo "$repo is too old"
    exit 1
  fi
done


