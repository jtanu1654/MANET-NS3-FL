#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/mobility-module.h"
#include "ns3/internet-module.h"
#include "ns3/wifi-module.h"
#include "ns3/aodv-module.h"
#include "ns3/olsr-module.h"
#include "ns3/dsdv-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"

using namespace ns3;

int main(int argc, char *argv[])
{
    uint32_t numNodes = 20;
    double speed = 5.0;
    std::string protocol = "AODV";

    CommandLine cmd;
    cmd.AddValue("protocol", "AODV | OLSR | DSDV", protocol);
    cmd.AddValue("nodes", "Number of nodes", numNodes);
    cmd.AddValue("speed", "Node speed", speed);
    cmd.Parse(argc, argv);

    SeedManager::SetSeed(1);

    // Create nodes
    NodeContainer nodes;
    nodes.Create(numNodes);

    // WiFi setup
    WifiHelper wifi;
    wifi.SetStandard(WIFI_STANDARD_80211b);

    YansWifiPhyHelper phy;
    YansWifiChannelHelper channel;

    channel.SetPropagationDelay("ns3::ConstantSpeedPropagationDelayModel");
    channel.AddPropagationLoss("ns3::FriisPropagationLossModel");

    phy.SetChannel(channel.Create());

    WifiMacHelper mac;
    mac.SetType("ns3::AdhocWifiMac");

    NetDeviceContainer devices = wifi.Install(phy, mac, nodes);

    // ================== ✅ FINAL MOBILITY FIX ==================
    MobilityHelper mobility;

    Ptr<RandomRectanglePositionAllocator> positionAlloc =
        CreateObject<RandomRectanglePositionAllocator>();

    positionAlloc->SetAttribute("X",
        StringValue("ns3::UniformRandomVariable[Min=0.0|Max=1000.0]"));
    positionAlloc->SetAttribute("Y",
        StringValue("ns3::UniformRandomVariable[Min=0.0|Max=1000.0]"));

    mobility.SetMobilityModel("ns3::RandomWaypointMobilityModel",
        "Speed", StringValue("ns3::UniformRandomVariable[Min=1.0|Max=" + std::to_string(speed) + "]"),
        "Pause", StringValue("ns3::ConstantRandomVariable[Constant=0.5]"),
        "PositionAllocator", PointerValue(positionAlloc));  // ✅ FIX

    mobility.Install(nodes);
    // ==========================================================

    // Internet stack
    InternetStackHelper internet;

    if (protocol == "AODV")
    {
        AodvHelper aodv;
        internet.SetRoutingHelper(aodv);
    }
    else if (protocol == "OLSR")
    {
        OlsrHelper olsr;
        internet.SetRoutingHelper(olsr);
    }
    else if (protocol == "DSDV")
    {
        DsdvHelper dsdv;
        internet.SetRoutingHelper(dsdv);
    }

    internet.Install(nodes);

    // IP addressing
    Ipv4AddressHelper ipv4;
    ipv4.SetBase("10.1.1.0", "255.255.255.0");
    Ipv4InterfaceContainer interfaces = ipv4.Assign(devices);

    // Server
    UdpEchoServerHelper server(9);
    ApplicationContainer serverApp = server.Install(nodes.Get(0));
    serverApp.Start(Seconds(1.0));
    serverApp.Stop(Seconds(10.0));

    // Multiple clients
    for (uint32_t i = 1; i <= 10 && i < numNodes; i++)
    {
        UdpEchoClientHelper client(interfaces.GetAddress(0), 9);

        client.SetAttribute("MaxPackets", UintegerValue(1000));
        client.SetAttribute("Interval", TimeValue(Seconds(0.01)));
        client.SetAttribute("PacketSize", UintegerValue(1024));

        ApplicationContainer clientApp = client.Install(nodes.Get(numNodes - i));

        clientApp.Start(Seconds(2.0));
        clientApp.Stop(Seconds(10.0));
    }

    // Flow monitor
    FlowMonitorHelper flowmon;
    Ptr<FlowMonitor> monitor = flowmon.InstallAll();

    Simulator::Stop(Seconds(12.0));
    Simulator::Run();

    monitor->CheckForLostPackets();

    std::map<FlowId, FlowMonitor::FlowStats> stats = monitor->GetFlowStats();

    double totalThroughput = 0;
    double totalPdr = 0;
    double totalDelay = 0;
    int flowCount = 0;

    for (auto &flow : stats)
    {
        double duration = flow.second.timeLastRxPacket.GetSeconds() -
                          flow.second.timeFirstTxPacket.GetSeconds();

        double throughput = 0;
        if (duration > 0)
            throughput = flow.second.rxBytes * 8.0 / duration / 1024;

        double pdr = 0;
        if (flow.second.txPackets > 0)
            pdr = (double)flow.second.rxPackets / flow.second.txPackets * 100;

        double delay = 0;
        if (flow.second.rxPackets > 0)
            delay = flow.second.delaySum.GetSeconds() / flow.second.rxPackets;

        totalThroughput += throughput;
        totalPdr += pdr;
        totalDelay += delay;
        flowCount++;
    }

    // Final output (used in dataset)
    if (flowCount > 0)
    {
        std::cout << "Throughput: " << totalThroughput / flowCount << std::endl;
        std::cout << "Packet Delivery Ratio: " << totalPdr / flowCount << std::endl;
        std::cout << "Average Delay: " << totalDelay / flowCount << std::endl;
    }

    Simulator::Destroy();
    return 0;
}