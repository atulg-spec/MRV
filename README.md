# Overview

This is a Blue Carbon Registry prototype that demonstrates an end-to-end Monitoring, Reporting, and Verification (MRV) system for blue carbon restoration projects. The application simulates the complete workflow from field data collection to carbon credit generation, including verification processes and blockchain-style transaction recording. It's designed as a hackathon demonstration piece showcasing how restoration organizations can digitally track mangrove and coastal ecosystem restoration efforts.

![Prototype Image](https://raw.githubusercontent.com/atulg-spec/MRV/main/static/img/prototypeimage.jpeg)


# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Single-page application** built with vanilla HTML, CSS, and JavaScript
- **Tailwind CSS via CDN** for responsive, utility-first styling
- **Component-based structure** using JavaScript functions to generate UI elements
- **Modal-driven interactions** for detailed views and admin functions
- **Local state management** using JavaScript objects and arrays
- **Event-driven architecture** with form submissions and button clicks triggering state updates

## Data Management
- **Browser localStorage** as the primary data persistence layer
- **JSON-based data structures** for restoration records, transactions, and settings
- **In-memory state** for UI state like modals, loading states, and temporary form data
- **Simulated IPFS integration** generating fake Content Identifiers (CIDs) for records
- **Deterministic carbon calculations** using seedling count, species factors, and age multipliers

## Core Workflows
- **Record Creation Flow**: Form-based data entry → validation → carbon estimation → localStorage storage → UI update
- **Verification Workflow**: Draft → Provisional → Verified → Credited status progression
- **Admin/Verifier Actions**: Role-based verification controls with simulated blockchain transactions
- **File Handling**: Image upload with preview functionality for photos and drone imagery

## UI/UX Design Patterns
- **Responsive layout** with mobile-first approach using Tailwind breakpoints
- **Card-based record display** for easy scanning and interaction
- **Toast notifications** for user feedback on actions
- **Loading states** with spinner animations for simulated async operations
- **Print-friendly styling** for generating reports and documentation

# External Dependencies

## CDN Dependencies
- **Tailwind CSS** - Utility-first CSS framework loaded via CDN for styling
- **Browser APIs** - FileReader API for image handling, localStorage for persistence

## Simulated Integrations
- **IPFS** - Generates fake Content Identifiers to simulate distributed storage
- **Blockchain** - Simulated on-chain transactions with fake transaction hashes
- **Verification Services** - Mock verification workflow with automated status updates

## File System
- **Image Handling** - Browser-based file upload and preview using FileReader API
- **Local Storage** - Browser localStorage for data persistence across sessions
- **Print System** - CSS print media queries for generating printable reports

The system is designed to be completely standalone without requiring backend services, making it ideal for demonstration purposes while showcasing the full MRV workflow concept.