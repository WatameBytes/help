import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import io.vertx.core.json.JsonObject;
import io.vertx.core.eventbus.Message;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

public class IdentityRequestValidatorTest {

    @Mock
    private Message<JsonObject> message;

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);
    }

    // Test for empty request
    @Test
    public void validateRequestGivenEmptyRequestExpectedFalse() {
        JsonObject body = new JsonObject();
        when(message.body()).thenReturn(body);

        boolean actual = IdentityValidator.validateIdentityRequest(message);
        assertFalse(actual);
    }

    // Positive tests for all individual methods
    @Test
    public void validateRequestWithValidUserIdExpectedTrue() {
        JsonObject body = new JsonObject().put("userId", "validUserId");
        when(message.body()).thenReturn(body);

        boolean actual = IdentityValidator.validateIdentityRequest(message);
        assertTrue(actual);
    }

    @Test
    public void validateRequestWithValidEmailAddressExpectedTrue() {
        JsonObject body = new JsonObject().put("emailAddress", "email@example.com");
        when(message.body()).thenReturn(body);

        boolean actual = IdentityValidator.validateIdentityRequest(message);
        assertTrue(actual);
    }

    @Test
    public void validateRequestWithValidCm15ExpectedTrue() {
        JsonObject body = new JsonObject().put("cm15", "123456789012345");
        when(message.body()).thenReturn(body);

        boolean actual = IdentityValidator.validateIdentityRequest(message);
        assertTrue(actual);
    }

    @Test
    public void validateRequestWithValidIdentityElementUserIdExpectedTrue() {
        JsonObject body = new JsonObject().put("identityElement", "validUserId");
        when(message.body()).thenReturn(body);

        boolean actual = IdentityValidator.validateIdentityRequest(message);
        assertTrue(actual);
    }

    @Test
    public void validateRequestWithValidIdentityElementEmailExpectedTrue() {
        JsonObject body = new JsonObject().put("identityElement", "email@example.com");
        when(message.body()).thenReturn(body);

        boolean actual = IdentityValidator.validateIdentityRequest(message);
        assertTrue(actual);
    }

    @Test
    public void validateRequestWithValidIdentityElementCm15ExpectedTrue() {
        JsonObject body = new JsonObject().put("identityElement", "123456789012345");
        when(message.body()).thenReturn(body);

        boolean actual = IdentityValidator.validateIdentityRequest(message);
        assertTrue(actual);
    }

    // Positive tests for claim token combinations
    @Test
    public void validateRequestWithValidClaimTokenAndUserIdExpectedTrue() {
        JsonObject body = new JsonObject()
            .put("claimToken", "someValidToken")
            .put("userId", "validUserId");
        when(message.body()).thenReturn(body);

        boolean actual = IdentityValidator.validateIdentityRequest(message);
        assertTrue(actual);
    }

    @Test
    public void validateRequestWithValidClaimTokenAndEmailAddressExpectedTrue() {
        JsonObject body = new JsonObject()
            .put("claimToken", "someValidToken")
            .put("emailAddress", "email@example.com");
        when(message.body()).thenReturn(body);

        boolean actual = IdentityValidator.validateIdentityRequest(message);
        assertTrue(actual);
    }

    @Test
    public void validateRequestWithValidClaimTokenAndCm15ExpectedTrue() {
        JsonObject body = new JsonObject()
            .put("claimToken", "someValidToken")
            .put("cm15", "123456789012345");
        when(message.body()).thenReturn(body);

        boolean actual = IdentityValidator.validateIdentityRequest(message);
        assertTrue(actual);
    }

    // Negative tests for missing fields
    @Test
    public void validateRequestMissingUserIdExpectedFalse() {
        JsonObject body = new JsonObject();
        when(message.body()).thenReturn(body);

        boolean actual = IdentityValidator.validateIdentityRequest(message);
        assertFalse(actual);
    }

    @Test
    public void validateRequestMissingEmailAddressExpectedFalse() {
        JsonObject body = new JsonObject();
        when(message.body()).thenReturn(body);

        boolean actual = IdentityValidator.validateIdentityRequest(message);
        assertFalse(actual);
    }

    @Test
    public void validateRequestMissingCm15ExpectedFalse() {
        JsonObject body = new JsonObject();
        when(message.body()).thenReturn(body);

        boolean actual = IdentityValidator.validateIdentityRequest(message);
        assertFalse(actual);
    }

    @Test
    public void validateRequestMissingIdentityElementExpectedFalse() {
        JsonObject body = new JsonObject();
        when(message.body()).thenReturn(body);

        boolean actual = IdentityValidator.validateIdentityRequest(message);
        assertFalse(actual);
    }

    @Test
    public void validateRequestMissingClaimTokenExpectedFalse() {
        JsonObject body = new JsonObject().put("userId", "validUserId"); // Missing claimToken
        when(message.body()).thenReturn(body);

        boolean actual = IdentityValidator.validateIdentityRequest(message);
        assertFalse(actual);
    }
}
