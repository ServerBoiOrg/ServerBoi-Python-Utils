import json
from discord import Embed, Color
from time import gmtime, strftime
from serverboi_utils.regions import ServiceRegion
from serverboi_utils.states import translate_state
import a2s
import socket


def form_workflow_embed(
    workflow_name: str,
    workflow_description: str,
    status: str,
    stage: str,
    color: Color,
    error: str = None,
) -> Embed:

    last_updated = f'⏱️ Last updated: {strftime("%H:%M:%S UTC", gmtime())}'

    embed = Embed(
        title=workflow_name,
        color=color,
        description=workflow_description,
    )

    if error:
        embed.add_field(name="Error", value=error, inline=False)
    embed.add_field(name="Status", value=status, inline=True)
    embed.add_field(name="Stage", value=stage, inline=True)
    embed.set_footer(text=last_updated)

    return embed


def get_thumbnail(game: str) -> str:
    thumbnails = {
        "ns2": "https://wiki.naturalselection2.com/images/c/c9/Cyst_grow.gif",
        "csgo": "https://thumbs.gfycat.com/AffectionateTastyFirefly-size_restricted.gif"
    }

    return thumbnails[game]


def form_server_embed(
    server_name: str,
    server_id: str,
    ip: str,
    port: str,
    status: str,
    region: ServiceRegion,
    game: str,
    owner: str,
    service: str,
) -> Embed:
    if ip is None:
        address = "No address while inactive"
        description = "\u200B"
    else:
        address = f"{ip}:{port}"
        description = f"Connect: steam://connect/{address}"

    state, state_emoji = translate_state(service, status)

    if state == "running":
        active = True
    else:
        active = False

    if active:
        query_port = int(port)
        try:
            info = a2s.info((ip, query_port))
            print(info)
        except socket.timeout:
            print("Trying next")
            try:
                info = a2s.info((ip, query_port + 1))
                description = "Direct connection not supported"
                print(info)
            except socket.timeout:
                player_value = "Error contacting server"
        except Exception as error:
            player_value = "Error contacting server"
            print(error)
        else:
            player_value = f"{info.player_count}/{info.max_players}"

    embed = Embed(
        title=f"{server_name} ({server_id})",
        color=Color.blurple(),
        description=description,
    )

    embed.set_thumbnail(
        url=get_thumbnail(game)
    )

    embed.add_field(name="Status", value=f"{state_emoji} {state}", inline=True)

    embed.add_field(name="\u200B", value=f"\u200B", inline=True)

    embed.add_field(name="Address", value=f"`{address}`", inline=True)

    embed.add_field(
        name="Location",
        value=f"{region.emoji} {region.sb_region} ({region.location})",
        inline=True,
    )

    if not active:
        embed.add_field(name="\u200B", value=f"\u200B", inline=True)

    embed.add_field(name="Game", value=game, inline=True)

    embed.add_field(name="Players", value=player_value, inline=True)

    embed.set_footer(
        text=f"Owner: {owner} | 🌎 Hosted on {service} in region {region.name} | 🕒 Pulled at {strftime('%H:%M:%S UTC', gmtime())}"
    )

    return embed
