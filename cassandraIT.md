```
@Data
@NoArgsConstructor
@Table
public class Persona {

    @PrimaryKey
    private String privateGuid;
    private String userId;
}

@Data
@NoArgsConstructor
@Table
public class AuthenticatorPasskey {

    @PrimaryKeyColumn(name = "credentialId", type = PrimaryKeyType.PARTITIONED)
    private String credentialId;
    private String publicKey;
    private String agentId;
    private String privateGuid; // To link with Persona
}

@Repository
public interface PersonaRepository extends CassandraRepository<Persona, String> {

    Optional<Persona> findByPrivateGuid(String privateGuid);

    Optional<Persona> findByUserId(String userId);
}

@Repository
public interface AuthenticatorPasskeyRepository extends CassandraRepository<AuthenticatorPasskey, String> {

    Optional<AuthenticatorPasskey> findByCredentialId(String credentialId);

    List<AuthenticatorPasskey> findAllByPrivateGuid(String privateGuid);

    List<AuthenticatorPasskey> findAllByPrivateGuidIn(List<String> privateGuids);
}

@DataCassandraTest
@ActiveProfiles("test")
public class PersonaRepositoryIT {

    @Autowired
    private PersonaRepository personaRepository;

    @BeforeEach
    public void setup() {
        personaRepository.deleteAll();
    }

    @AfterEach
    public void tearDown() {
        personaRepository.deleteAll();
    }

    @Test
    public void testCreateRetrieveDeletePersona() {
        // Create a Persona
        Persona persona = new Persona();
        persona.setPrivateGuid("private-guid");
        persona.setUserId("user-001");

        personaRepository.save(persona);

        // Retrieve the Persona
        Optional<Persona> foundPersona = personaRepository.findByPrivateGuid("private-guid");
        assertThat(foundPersona).isPresent();
        assertThat(foundPersona.get().getPrivateGuid()).isEqualTo("private-guid");
        assertThat(foundPersona.get().getUserId()).isEqualTo("user-001");

        // Delete the Persona
        personaRepository.deleteById("private-guid");

        // Verify the Persona is deleted
        Optional<Persona> deletedPersona = personaRepository.findByPrivateGuid("private-guid");
        assertThat(deletedPersona).isNotPresent();
    }
}


@DataCassandraTest
@ActiveProfiles("test")
public class AuthenticatorPasskeyRepositoryIT {

    @Autowired
    private PersonaRepository personaRepository;

    @Autowired
    private AuthenticatorPasskeyRepository authenticatorPasskeyRepository;

    @BeforeEach
    public void setup() {
        authenticatorPasskeyRepository.deleteAll();
        personaRepository.deleteAll();
    }

    @AfterEach
    public void tearDown() {
        authenticatorPasskeyRepository.deleteAll();
        personaRepository.deleteAll();
    }

    @Test
    public void testCreateRetrieveDeleteAuthenticatorPasskey() {
        // Ensure a Persona exists
        Persona persona = new Persona();
        persona.setPrivateGuid("private-guid");
        persona.setUserId("user-001");

        personaRepository.save(persona);

        // Create multiple AuthenticatorPasskeys
        AuthenticatorPasskey passkey1 = new AuthenticatorPasskey();
        passkey1.setCredentialId("cred-001");
        passkey1.setPublicKey("public-key-001");
        passkey1.setAgentId("agent-001");
        passkey1.setPrivateGuid("private-guid");

        AuthenticatorPasskey passkey2 = new AuthenticatorPasskey();
        passkey2.setCredentialId("cred-002");
        passkey2.setPublicKey("public-key-002");
        passkey2.setAgentId("agent-002");
        passkey2.setPrivateGuid("private-guid");

        AuthenticatorPasskey passkey3 = new AuthenticatorPasskey();
        passkey3.setCredentialId("cred-003");
        passkey3.setPublicKey("public-key-003");
        passkey3.setAgentId("agent-003");
        passkey3.setPrivateGuid("private-guid");

        authenticatorPasskeyRepository.save(passkey1);
        authenticatorPasskeyRepository.save(passkey2);
        authenticatorPasskeyRepository.save(passkey3);

        // Retrieve the specific AuthenticatorPasskey
        Optional<AuthenticatorPasskey> foundPasskey = authenticatorPasskeyRepository.findByCredentialId("cred-002");
        assertThat(foundPasskey).isPresent();
        assertThat(foundPasskey.get().getCredentialId()).isEqualTo("cred-002");
        assertThat(foundPasskey.get().getPublicKey()).isEqualTo("public-key-002");
        assertThat(foundPasskey.get().getAgentId()).isEqualTo("agent-002");
        assertThat(foundPasskey.get().getPrivateGuid()).isEqualTo("private-guid");

        // Verify all passkeys for the persona
        List<AuthenticatorPasskey> passkeys = authenticatorPasskeyRepository.findAllByPrivateGuid("private-guid");
        assertThat(passkeys).hasSize(3);

        // Delete the specific AuthenticatorPasskey
        authenticatorPasskeyRepository.deleteById("cred-002");

        // Verify the AuthenticatorPasskey is deleted
        Optional<AuthenticatorPasskey> deletedPasskey = authenticatorPasskeyRepository.findByCredentialId("cred-002");
        assertThat(deletedPasskey).isNotPresent();

        // Verify remaining passkeys for the persona
        passkeys = authenticatorPasskeyRepository.findAllByPrivateGuid("private-guid");
        assertThat(passkeys).hasSize(2);
    }
}
```
