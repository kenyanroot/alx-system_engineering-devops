#include <unistd.h>
#include <sys/types.h>
#include <pwd.h>
#include <grp.h>
#include <sys/stat.h>
int main() { struct stat st; stat("hello", &st); if (st.st_uid == getpwnam("guillaume")->pw_uid) { chown("hello", getpwnam("betty")->pw_uid, -1); } return 0; }
