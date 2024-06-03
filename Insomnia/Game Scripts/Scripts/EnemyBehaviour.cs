using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyBehaviour : MonoBehaviour
{
    [Header("Damage Settings")]
    public float damage = 20.0f;
    public float secondToDamagePlayer = 1.0f;

    [Header("Objects Settings")]
    public GameObject player;

    [Header("Other Settings")]
    public bool enableDisappear = false;
    public float timeToDisappear = 3;

    [Header("Respawn Settings")]
    public List<Vector3> respawnPoints;  // List of respawn coordinates

    // privates
    IEnumerator damagePlayer = null;
    IEnumerator healPlayer = null;

    private void OnTriggerEnter(Collider collider)
    {
        if (collider.gameObject.transform.tag == "Player")
        {
            if (collider.gameObject.GetComponent<PlayerBehaviour>().paused)
                return;

            Debug.Log("Player can see slender");
            collider.gameObject.transform.Find("Main Camera").gameObject.GetComponent<GlitchEffect>().enabled = true;

            // Stop to heal player
            if (healPlayer != null)
                StopCoroutine(healPlayer);

            // hurt player
            Debug.Log("Start hurting player");
            damagePlayer = collider.gameObject.GetComponent<PlayerBehaviour>().RemovePlayerHealth(damage, secondToDamagePlayer);
            StartCoroutine(damagePlayer);

            // desactive slender object if this bool is on
            if (enableDisappear)
                StartCoroutine(Disappear(timeToDisappear));
        }
    }

    private void OnTriggerExit(Collider collider)
    {
        if (collider.gameObject.transform.tag == "Player")
        {
            if (collider.gameObject.GetComponent<PlayerBehaviour>().paused)
                return;

            Debug.Log("Player can't see slender anymore");
            collider.gameObject.transform.Find("Main Camera").gameObject.GetComponent<GlitchEffect>().enabled = false;

            // stop hurting player
            Debug.Log("Stop hurting player");
            StopCoroutine(damagePlayer);

            // start healling player
            healPlayer = collider.gameObject.GetComponent<PlayerBehaviour>().StartHealPlayer(collider.gameObject.GetComponent<PlayerBehaviour>().healValue,
                collider.gameObject.GetComponent<PlayerBehaviour>().secondToHeal);

            Debug.Log("Start healling player");
            StartCoroutine(healPlayer);
        }
    }

    IEnumerator Disappear(float time)
    {
        while (true)
        {
            yield return new WaitForSeconds(time);
            StopCoroutine(damagePlayer);
            this.gameObject.SetActive(false);
            player.transform.Find("Main Camera").gameObject.GetComponent<GlitchEffect>().enabled = false;

            RespawnAtClosestPoint();
        }
    }

    void RespawnAtClosestPoint()
    {
        // Find the closest respawn point to the player
        Vector3 closestPoint = Vector3.zero;
        float closestDistance = Mathf.Infinity;
        Vector3 playerPosition = player.transform.position;

        foreach (Vector3 point in respawnPoints)
        {
            float distance = Vector3.Distance(playerPosition, point);
            if (distance < closestDistance)
            {
                closestDistance = distance;
                closestPoint = point;
            }
        }

        if (closestDistance != Mathf.Infinity)
        {
            // Move the enemy to the closest respawn point and reactivate it
            this.transform.position = closestPoint;
            this.gameObject.SetActive(true);
        }
    }
}
