// Local lab only. Invoked from JENKINS_HOME/init.groovy.d by setup-lab.py.
import jenkins.model.Jenkins
import jenkins.model.JenkinsLocationConfiguration
import hudson.model.JDK
import hudson.tasks.Maven
import hudson.security.HudsonPrivateSecurityRealm
import hudson.security.FullControlOnceLoggedInAuthorizationStrategy
import jenkins.install.InstallState

def j = Jenkins.get()
def lab = j.rootDir.parentFile
def repo = lab.parentFile
if (!j.isUseSecurity()) {
    def realm = new HudsonPrivateSecurityRealm(false)
    realm.createAccount('lab-admin', new File(lab, 'admin-password').text.trim())
    j.setSecurityRealm(realm)
    def auth = new FullControlOnceLoggedInAuthorizationStrategy()
    auth.setAllowAnonymousRead(true)
    j.setAuthorizationStrategy(auth)
}
j.setNumExecutors(1)
j.setJDKs([new JDK('JDK-21', '/usr/lib/jvm/java-21-openjdk-amd64')])
def md = j.getDescriptorByType(Maven.DescriptorImpl.class)
md.setInstallations(new Maven.MavenInstallation('Maven-3.9', new File(lab, 'tools/apache-maven-3.9.16').absolutePath, []))
md.save()
JenkinsLocationConfiguration.get().setUrl('http://localhost:8080/')
JenkinsLocationConfiguration.get().save()
['hello-world-job','deploy-job','java-maven-freestyle'].each { name ->
    if (j.getItem(name) == null) {
        def xml = new File(repo, "jenkins/${name}.xml").text.replace('@LAB_ROOT@', repo.absolutePath)
        j.createProjectFromXML(name, new ByteArrayInputStream(xml.getBytes('UTF-8')))
    }
}
j.setInstallState(InstallState.INITIAL_SETUP_COMPLETED)
j.save()
